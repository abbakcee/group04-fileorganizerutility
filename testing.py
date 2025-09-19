


from pathlib import Path
import json
import shutil
import src.organizer as organizer

def test_propose_moves(tmp_path):
    # create sample files
    f1 = tmp_path / "a.txt"
    f1.write_text("hello")
    f2 = tmp_path / "b.jpg"
    f2.write_text("img")
    mapping = organizer.propose_moves(tmp_path)
    # mapping keys should be full paths as strings
    assert str(f1) in mapping
    assert str(f2) in mapping
    # targets should contain folder names
    assert "Documents" in mapping[str(f1)] or "Documents" == organizer.categorize_by_extension(f1)
    assert "Images" in mapping[str(f2)] or "Images" == organizer.categorize_by_extension(f2)

def test_perform_and_undo(tmp_path):
    # create files
    f1 = tmp_path / "note.txt"
    f1.write_text("x")
    f2 = tmp_path / "pic.png"
    f2.write_text("y")
    mapping = organizer.propose_moves(tmp_path)
    history_dir = tmp_path / ".history"
    # perform moves
    undo_file = organizer.perform_moves(mapping, history_dir=history_dir)
    assert undo_file.exists()
    # ensure files moved
    moved_targets = [p for p in (tmp_path / "Documents").glob("*")] if (tmp_path / "Documents").exists() else []
    moved_images = [p for p in (tmp_path / "Images").glob("*")] if (tmp_path / "Images").exists() else []
    assert any("note" in str(p) for p in moved_targets)
    assert any("pic" in str(p) for p in moved_images)
    # undo
    ts, undone = organizer.undo_last_move(history_dir=history_dir)
    # after undo, original files should be back in tmp_path
    assert (tmp_path / "note.txt").exists()
    assert (tmp_path / "pic.png").exists()


