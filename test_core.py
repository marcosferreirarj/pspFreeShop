import os
import pytest
import core

def test_parse_tsv(tmp_path):
    # Cria um TSV falso no tmp_path do pytest
    tsv_content = (
        "Title ID\tRegion\tType\tName\tPKG direct link\tContent ID\tLast Modification Date\tRAP\tDownload .RAP file\tFile Size\tSHA256\n"
        "NPUG80330\tUS\tPSP\tJak and Daxter\thttp://zeus.dl.playstation.net/test.pkg\tUP9000-NPUG80330_00-0000\t2021-04-23\tRAP_STRING_123\t\t1000\tsha256\n"
        "NPUG80000\tUS\tPSP\tEmpty PKG Test\t\tUP9000\t\t\t\t\t\n"
    )
    
    test_tsv = tmp_path / "PSP_GAMES.tsv"
    test_tsv.write_text(tsv_content, encoding='utf-8')
    
    games = core.parse_tsv(str(test_tsv))
    
    # O segundo jogo deve ser ignorado pois nao tem link
    assert len(games) == 1
    
    game = games[0]
    assert game["title_id"] == "NPUG80330"
    assert game["name"] == "Jak and Daxter"
    assert game["pkg_link"] == "http://zeus.dl.playstation.net/test.pkg"
    assert game["zrif_rap"] == "RAP_STRING_123"

def test_transfer_to_psp_iso(tmp_path):
    temp_dir = tmp_path / "temp_extract"
    temp_dir.mkdir()
    
    # Fake extracted ISO
    iso_file = temp_dir / "Game.iso"
    iso_file.write_text("dummy")
    
    usb_drive = tmp_path / "USB"
    usb_drive.mkdir()
    
    core.transfer_to_psp(str(temp_dir), str(usb_drive))
    
    # Check if ISO dir is created and file moved
    assert (usb_drive / "ISO" / "Game.iso").exists()
    assert not iso_file.exists()

def test_transfer_to_psp_eboot(tmp_path):
    temp_dir = tmp_path / "temp_extract"
    temp_dir.mkdir()
    
    # Fake extracted EBOOT inside TitleID folder
    title_folder = temp_dir / "NPUG80330"
    title_folder.mkdir()
    
    eboot_file = title_folder / "EBOOT.PBP"
    eboot_file.write_text("dummy eboot")
    
    usb_drive = tmp_path / "USB"
    usb_drive.mkdir()
    
    core.transfer_to_psp(str(temp_dir), str(usb_drive))
    
    # Check if PSP/GAME/TitleID dir is created and file moved
    dest_eboot = usb_drive / "PSP" / "GAME" / "NPUG80330" / "EBOOT.PBP"
    assert dest_eboot.exists()
    assert not title_folder.exists()
