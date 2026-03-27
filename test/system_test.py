from iesude.data import MitBihAtrialFibrillationDataSet 
from pathlib import Path
import shutil

def test_downloading_atrialfibrillation_dataset():
    dataset_dir = Path(__file__).parent.parent /"test_artifacts/atrialfibrillation"
    if dataset_dir.exists():
        shutil.rmtree(dataset_dir)
    MitBihAtrialFibrillationDataSet.download_if_missing(dataset_dir)
    assert dataset_dir.exists()