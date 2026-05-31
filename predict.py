import sys
import time
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
from typing import Dict, Union, List, Optional, Tuple

class SurrogatePredictor:
    """
    Surrogate model predictor using an ensemble of 20 MLP models.
    Provides mean predictions and uncertainty (standard deviation).
    """
    def __init__(self, model_path: Optional[Path] = None):
        """
        Initialize the predictor by loading the ensemble and scalers.
        Args:
            model_path: Path to the model directory. If None, uses default ROOT/models/
        """
        if model_path is None:
            if 'ipykernel' in sys.modules:
                ROOT = Path().resolve()
            else:
                ROOT = Path(__file__).parent
            model_path = ROOT / "models"
        self.model_path = Path(model_path)
        self.scaler_path = self.model_path / "scalers"
        
        # Load ensemble and scalers
        print(f"Loading ensemble from : {self.model_path}")
        try:
            # Load list of 20 models
            self.models = joblib.load(self.model_path / "ensemble_20_models.pkl")
            self.scaler_X = joblib.load(self.scaler_path / "scaler_X.pkl")
            self.scaler_Y = joblib.load(self.scaler_path / "scaler_Y.pkl")
            
            self.n_models = len(self.models)
            print(f"Loaded {self.n_models} models in ensemble")
            
            # Feature and target names
            self.feature_names = ['beam_height', 'beam_length', 'fillet_size', 'beam_width']
            self.target_names  = ['modal_frequency_1','modal_frequency_2','modal_frequency_3',
                                  'modal_frequency_4','max_deformation','max_stress']
        except Exception as e:
            print(f"[ERROR] {e}")
            raise
    
    def _predict_scaled(self, X_scaled: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict scaled outputs and compute mean and std across ensemble.
        Returns: (mean_scaled, std_scaled) each of shape (n_samples, n_outputs)
        """
        # Get predictions from all models: shape (n_models, n_samples, n_outputs)
        preds = np.array([model.predict(X_scaled) for model in self.models])
        mean_scaled = np.mean(preds, axis=0)
        std_scaled = np.std(preds, axis=0)
        return mean_scaled, std_scaled
    
    def predict_with_uncertainty(self,
                                 beam_height: Union[float, List[float], np.ndarray],
                                 beam_length: Union[float, List[float], np.ndarray],
                                 fillet_size: Union[float, List[float], np.ndarray],
                                 beam_width: Union[float, List[float], np.ndarray],
                                 return_dataframe: bool = True
                                 ) -> Tuple[Union[pd.DataFrame, np.ndarray],
                                            Union[pd.DataFrame, np.ndarray]]:
        """
        Predict outputs and their standard deviation (uncertainty).
        
        Args:
            beam_height, beam_length, fillet_size, beam_width: input parameters.
            return_dataframe: If True, returns DataFrames; else numpy arrays.
        
        Returns:
            (mean_predictions, std_predictions) in original physical units.
        """
        # Convert single values to arrays
        if isinstance(beam_height, (int, float)):
            beam_height = [beam_height]
            beam_length = [beam_length]
            fillet_size = [fillet_size]
            beam_width = [beam_width]
        
        X_input = np.column_stack([beam_height, beam_length, fillet_size, beam_width])
        self._validate_inputs(X_input)
        
        # Scale inputs
        X_scaled = self.scaler_X.transform(X_input)
        
        # Ensemble predictions in scaled space
        mean_scaled, std_scaled = self._predict_scaled(X_scaled)
        
        # Inverse transform mean to physical units
        mean_phys = self.scaler_Y.inverse_transform(mean_scaled)
        # Std scales by the scaler's scale factor (linear transform)
        std_phys = std_scaled * self.scaler_Y.scale_
        
        if return_dataframe:
            mean_df = pd.DataFrame(mean_phys, columns=self.target_names)
            std_df = pd.DataFrame(std_phys, columns=[f"{t}_std" for t in self.target_names])
            return mean_df, std_df
        else:
            return mean_phys, std_phys
    
    def predict(self,
                beam_height: Union[float, List[float], np.ndarray],
                beam_length: Union[float, List[float], np.ndarray],
                fillet_size: Union[float, List[float], np.ndarray],
                beam_width: Union[float, List[float], np.ndarray],
                return_dataframe: bool = True) -> Union[pd.DataFrame, np.ndarray]:
        """
        Predict outputs (mean only) – backward compatible interface.
        """
        mean, _ = self.predict_with_uncertainty(beam_height, beam_length,
                                                fillet_size, beam_width,
                                                return_dataframe)
        return mean
    
    def predict_single(self,
                       beam_height: float,
                       beam_length: float,
                       fillet_size: float,
                       beam_width: float) -> Dict[str, float]:
        """
        Convenience method for single prediction returning mean dictionary.
        """
        mean_df, _ = self.predict_with_uncertainty(beam_height, beam_length,
                                                   fillet_size, beam_width,
                                                   return_dataframe=True)
        return mean_df.iloc[0].to_dict()
    
    def predict_single_with_uncertainty(self,
                                    beam_height: float,
                                    beam_length: float,
                                    fillet_size: float,
                                    beam_width: float) -> Dict[str, Dict[str, float]]:
        """
        Single prediction with uncertainty.
        Returns: {'mean': {target: value}, 'std': {target: value}} 
                (std dict uses same target names)
        """
        mean_df, std_df = self.predict_with_uncertainty(beam_height, beam_length,
                                                        fillet_size, beam_width,
                                                        return_dataframe=True)
        # Strip '_std' suffix from std_df column names
        std_df.columns = [col.replace('_std', '') for col in std_df.columns]
        return {'mean': mean_df.iloc[0].to_dict(),
                'std': std_df.iloc[0].to_dict()}
    
    def predict_batch(self, df_input: pd.DataFrame) -> pd.DataFrame:
        """
        Predict from DataFrame (mean only).
        """
        mean_df, _ = self.predict_with_uncertainty(df_input['beam_height'].values,
                                                   df_input['beam_length'].values,
                                                   df_input['fillet_size'].values,
                                                   df_input['beam_width'].values,
                                                   return_dataframe=True)
        return mean_df
    
    def predict_batch_with_uncertainty(self, df_input: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Batch prediction with uncertainty.
        Returns: (mean_df, std_df)
        """
        return self.predict_with_uncertainty(df_input['beam_height'].values,
                                             df_input['beam_length'].values,
                                             df_input['fillet_size'].values,
                                             df_input['beam_width'].values,
                                             return_dataframe=True)
    
    def _validate_inputs(self, X: np.ndarray):
        """Validate that inputs are within training range (approx)."""
        for i, (feature, mean, scale) in enumerate(zip(
            self.feature_names,
            self.scaler_X.mean_,
            self.scaler_X.scale_
        )):
            # Approximate original range as mean ± 3*scale
            actual_min = mean - 3*scale
            actual_max = mean + 3*scale
            if np.any(X[:, i] < actual_min) or np.any(X[:, i] > actual_max):
                print(f"⚠️  Warning: {feature} value outside training range")
                print(f"   Training range: [{actual_min:.2f}, {actual_max:.2f}]")
                print(f"   Input values: [{X[:, i].min():.2f}, {X[:, i].max():.2f}]")


# ==================== USAGE EXAMPLES WITH TIME PROFILING ====================
# The following code runs only when the script is executed directly (or in a notebook).
if __name__ == "__main__" or 'ipykernel' in sys.modules:
    print("="*80)
    print("ENSEMBLE SURROGATE MODEL PREDICTOR (20 models) - TIME PROFILING")
    print("="*80)
    
    # ------------------------------------------------------------------
    # 1. Model loading time
    # ------------------------------------------------------------------
    load_start = time.perf_counter()
    predictor = SurrogatePredictor()
    load_end = time.perf_counter()
    load_time = load_end - load_start
    print(f"Model loading time: {load_time:.4f} seconds")
    
    # ------------------------------------------------------------------
    # 2. Single prediction (with uncertainty) timing
    # ------------------------------------------------------------------
    print("\n" + "="*80)
    print("CASE 1: Single prediction (one sample)")
    print("="*80)
    
    single_start = time.perf_counter()
    result_single = predictor.predict_single_with_uncertainty(
        beam_height=10.0,
        beam_length=12.5,
        fillet_size=0.3,
        beam_width=0.6
    )
    single_end = time.perf_counter()
    single_time = single_end - single_start
    
    # Display results
    print("\nInput parameters:")
    print(f"  beam_height = 10.0 mm")
    print(f"  beam_length = 12.5 mm")
    print(f"  fillet_size = 0.3 mm")
    print(f"  beam_width  = 0.6 mm")
    
    print("\nPredictions (mean ± std):")
    for target in predictor.target_names:
        mean_val = result_single['mean'][target]
        std_val = result_single['std'][target]
        if 'frequency' in target:
            print(f"  {target:30}: {mean_val:.2f} ± {std_val:.2f} Hz")
        elif 'deformation' in target:
            print(f"  {target:30}: {mean_val:.6f} ± {std_val:.6f} mm")
        elif 'stress' in target:
            print(f"  {target:30}: {mean_val:.3f} ± {std_val:.3f} MPa")
        else:
            print(f"  {target:30}: {mean_val:.3f} ± {std_val:.3f}")
    
    print(f"\n  Single prediction time: {single_time*1000:.2f} ms")
    
    # ------------------------------------------------------------------
    # 3. Batch prediction (multiple samples) timing
    # ------------------------------------------------------------------
    print("\n" + "="*80)
    print("CASE 2: Batch prediction (3 samples)")
    print("="*80)
    
    test_inputs = pd.DataFrame({
        'beam_height': [8.0, 12.0, 16.0],
        'beam_length': [11.0, 13.0, 15.0],
        'fillet_size': [0.2, 0.4, 0.5],
        'beam_width': [0.5, 0.6, 0.7]
    })
    n_batch = len(test_inputs)
    
    print(f"\nInput DataFrame ({n_batch} samples):")
    print(test_inputs.to_string(index=False))
    
    batch_start = time.perf_counter()
    mean_df, std_df = predictor.predict_batch_with_uncertainty(test_inputs)
    batch_end = time.perf_counter()
    batch_time = batch_end - batch_start
    
    print("\nMean predictions (rounded):")
    print(mean_df.round(4).to_string(index=False))
    print("\nUncertainty (std dev):")
    print(std_df.round(4).to_string(index=False))
    
    print(f"\n  Batch prediction time ({n_batch} samples): {batch_time*1000:.2f} ms")
    print(f"   -> Average per sample: {batch_time/n_batch*1000:.2f} ms")
    
    # ------------------------------------------------------------------
    # 4. Sequential single predictions (3 calls) – overhead demonstration
    # ------------------------------------------------------------------
    print("\n" + "="*80)
    print("CASE 3: Sequential single predictions (3 separate calls)")
    print("="*80)
    
    # Use same inputs as batch for fair comparison
    sequential_start = time.perf_counter()
    for i in range(n_batch):
        _ = predictor.predict_single_with_uncertainty(
            beam_height=test_inputs.iloc[i]['beam_height'],
            beam_length=test_inputs.iloc[i]['beam_length'],
            fillet_size=test_inputs.iloc[i]['fillet_size'],
            beam_width=test_inputs.iloc[i]['beam_width']
        )
    sequential_end = time.perf_counter()
    sequential_time = sequential_end - sequential_start
    
    print(f"  {n_batch} sequential single calls: {sequential_time*1000:.2f} ms")
    print(f"   -> Average per call: {sequential_time/n_batch*1000:.2f} ms")
    
    # ------------------------------------------------------------------
    # 5. Batch with a single sample – to isolate overhead
    # ------------------------------------------------------------------
    print("\n" + "="*80)
    print("CASE 4: Batch prediction with 1 sample (overhead measurement)")
    print("="*80)
    
    single_sample_df = test_inputs.iloc[[0]]  # DataFrame with one row
    batch_single_start = time.perf_counter()
    _, _ = predictor.predict_batch_with_uncertainty(single_sample_df)
    batch_single_end = time.perf_counter()
    batch_single_time = batch_single_end - batch_single_start
    
    print(f"  Batch API with 1 sample: {batch_single_time*1000:.2f} ms")
    
    # ------------------------------------------------------------------
    # 6. Comparison Table
    # ------------------------------------------------------------------
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON & RECOMMENDATIONS")
    print("="*80)
    
    # Calculate metrics
    single_per_sample = single_time  # time for 1 sample via single API
    batch_per_sample = batch_time / n_batch
    sequential_per_sample = sequential_time / n_batch
    batch_single_overhead = batch_single_time  # time for batch API with 1 sample
    
    # Speedups
    speedup_batch_vs_single = single_per_sample / batch_per_sample if batch_per_sample > 0 else float('inf')
    speedup_batch_vs_sequential = sequential_per_sample / batch_per_sample if batch_per_sample > 0 else float('inf')
    
    # Create comparison table
    print("\n{:<35} {:>15} {:>15} {:>20}".format(
        "Prediction Method", "Total Time (ms)", "Per Sample (ms)", "Relative Speedup"
    ))
    print("-" * 85)
    
    print("{:<35} {:>15.2f} {:>15.2f} {:>20.1f}x".format(
        "Single API (1 sample)", single_time*1000, single_time*1000, 1.0
    ))
    print("{:<35} {:>15.2f} {:>15.2f} {:>20.1f}x".format(
        f"Batch API ({n_batch} samples)", batch_time*1000, batch_per_sample*1000, speedup_batch_vs_single
    ))
    print("{:<35} {:>15.2f} {:>15.2f} {:>20.1f}x".format(
        f"Sequential singles ({n_batch} calls)", sequential_time*1000, sequential_per_sample*1000, speedup_batch_vs_sequential
    ))
    print("{:<35} {:>15.2f} {:>15} {:>20}".format(
        "Batch API (1 sample)", batch_single_time*1000, "N/A", "overhead test"
    ))
    
    # ------------------------------------------------------------------
    # 7. System integration recommendations
    # ------------------------------------------------------------------
    print("\n" + "="*80)
    print("RECOMMENDATIONS FOR SYSTEMS INTEGRATION")
    print("="*80)
    
    print("""
     **Batch processing** is always preferred when you have multiple samples.
       - Use `predict_batch_with_uncertainty()` with DataFrames or arrays.
       - Typical speedup: ~{:.1f}x faster per sample compared to sequential singles.
    
     **For real-time / streaming applications**:
       - Buffer incoming requests (e.g., collect 5–10 samples) and predict in batch.
       - If single prediction is unavoidable, the cost is still low (~{:.2f} ms).
    
     **Overhead insight**:
       - Batch API even with 1 sample takes ~{:.2f} ms – very close to single API.
       - The main inefficiency is calling the API repeatedly, not the batch size itself.
    
     **Scaling behavior**:
       - Prediction time scales roughly linearly with batch size (vectorized).
       - Fixed overhead per batch call is about {:.2f} ms (from case 4).
    
     **Production tip**:
       - Load the predictor once at application startup (as done here).
       - Reuse the same instance for all predictions.
    """.format(
        speedup_batch_vs_sequential,
        single_time*1000,
        batch_single_time*1000,
        batch_single_time*1000
    ))
    
    print("\n" + "="*80)
    print("[Done] Profiling complete. Ensemble predictor ready for integration!")
    print("="*80)