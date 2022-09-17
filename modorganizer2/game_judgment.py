from __future__ import annotations

import os

import mobase
from PyQt5.QtCore import QFileInfo

from ..basic_game import BasicGame
from .yakuza.yakuza_series import YakuzaGameModDataChecker, yakuza_check_rmm, yakuza_import_mods


class JudgmentGame(BasicGame):

    __yakuza_exe_dir = os.path.join('runtime', 'media')

    Name = "Judgment Support Plugin"
    Author = "SutandoTsukai181"
    Version = "1.0.0"

    GameName = "Judgment"
    GameShortName = "judgment"
    GameSteamId = [2058180]
    GameBinary = os.path.join(__yakuza_exe_dir, "Judgment.exe")
    GameDataPath = os.path.join(__yakuza_exe_dir, 'mods', '_externalMods')

    def init(self, organizer: mobase.IOrganizer):
        super().init(organizer)
        self._featureMap[mobase.ModDataChecker] = YakuzaGameModDataChecker(self.__valid_paths)
        self._organizer.onUserInterfaceInitialized(lambda win: yakuza_check_rmm(self, win))
        self._organizer.onUserInterfaceInitialized(lambda win: yakuza_import_mods(self, win))
        return True

    def executables(self) -> list[mobase.ExecutableInfo]:
        return super().executables() + [mobase.ExecutableInfo(
            "Ryu Mod Manager",
            QFileInfo(self.gameDirectory().absoluteFilePath(
                os.path.join(self.__yakuza_exe_dir, 'RyuModManager.exe')))
        ).withArgument('--cli')]

    def settings(self) -> list[mobase.PluginSetting]:
        return super().settings() + [mobase.PluginSetting(
            'import_mods_prompt',
            'Check for mods to import from RMM mods folder on launch',
            True
        )]

    __valid_paths = {
        '3dlut',
        'artisan',
        'asset',
        'asset.par',
        'auth',
        'battle',
        'boot',
        'camera',
        'chara',
        'chara.par',
        'cmm',
        'cmm.par',
        'cubemap_judge',
        'cubemap_judge.par',
        'db.judge.de',
        'db.judge.de.par',
        'db.judge.en',
        'db.judge.en.par',
        'db.judge.es',
        'db.judge.es.par',
        'db.judge.fr',
        'db.judge.fr.par',
        'db.judge.it',
        'db.judge.it.par',
        'db.judge.ja',
        'db.judge.ja.par',
        'db.judge.ko',
        'db.judge.ko.par',
        'db.judge.zh',
        'db.judge.zh.par',
        'db.judge.zhs',
        'db.judge.zhs.par',
        'effect',
        'effect.par',
        'entity_table',
        'entity_judge',
        'entity_judge.par',
        'flood',
        'font.judge',
        'font.judge.par',
        'grass',
        'hact_judge',
        'light_anim_judge',
        'light_anim_judge.par',
        'lua',
        'lua.par',
        'map',
        'map.par',
        'minigame',
        'motion',
        'motion.par',
        'movie',
        'movie.par',
        'navimesh',
        'navimesh.par',
        'particle',
        'particle.par',
        'patch',
        'ps5',
        'puid.judge',
        'reflection',
        'shader',
        'sound',
        'sound.par',
        'sound_en',
        'sound_en.par',
        'stage',
        'stage_judge',
        'stream',
        'stream.par',
        'stream_en',
        'stream_en.par',
        'system',
        'talk_judge',
        'talk_judge.par',
        'ui.judge.de',
        'ui.judge.de.par',
        'ui.judge.en',
        'ui.judge.en.par',
        'ui.judge.es',
        'ui.judge.es.par',
        'ui.judge.fr',
        'ui.judge.fr.par',
        'ui.judge.it',
        'ui.judge.it.par',
        'ui.judge.ja',
        'ui.judge.ja.par',
        'ui.judge.ko',
        'ui.judge.ko.par',
        'ui.judge.zh',
        'ui.judge.zh.par',
        'ui.judge.zhs',
        'ui.judge.zhs.par',
        'version',
    }
