from __future__ import annotations

import os

import mobase
from PyQt5.QtCore import QFileInfo

from ..basic_game import BasicGame
from .yakuza.yakuza_series import YakuzaGameModDataChecker, yakuza_check_rmm, yakuza_import_mods


class LostJudgmentGame(BasicGame):

    __yakuza_exe_dir = os.path.join('runtime', 'media')

    Name = "Lost Judgment Support Plugin"
    Author = "SutandoTsukai181"
    Version = "1.0.0"

    GameName = "Lost Judgment"
    GameShortName = "lostjudgment"
    GameSteamId = [2058190]
    GameBinary = os.path.join(__yakuza_exe_dir, "LostJudgment.exe")
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
        'asset_coyote_ngen',
        'asset_coyote_ngen.par',
        'auth',
        'auth_dlc',
        'auth_hires',
        'auth_hires_dlc',
        'battle',
        'boot',
        'camera',
        'chara',
        'chara.par',
        'chara2',
        'chara2.par',
        'cubemap_coyote',
        'cubemap_coyote.par',
        'db.coyote.de',
        'db.coyote.de.par',
        'db.coyote.en',
        'db.coyote.en.par',
        'db.coyote.es',
        'db.coyote.es.par',
        'db.coyote.fr',
        'db.coyote.fr.par',
        'db.coyote.it',
        'db.coyote.it.par',
        'db.coyote.ja',
        'db.coyote.ja.par',
        'db.coyote.ko',
        'db.coyote.ko.par',
        'db.coyote.zh',
        'db.coyote.zh.par',
        'db.coyote.zhs',
        'db.coyote.zhs.par',
        'effect',
        'effect.par',
        'entity_table',
        'entity_coyote',
        'entity_coyote.par',
        'flood',
        'font.coyote',
        'font.coyote.par',
        'grass',
        'hact_coyote',
        'light_anim_coyote',
        'light_anim_coyote.par',
        'lua',
        'lua.par',
        'map',
        'map.par',
        'minigame',
        'motion',
        'motion.par',
        'moviesd',
        'moviesd.par',
        'moviesd_dlc',
        'moviesd_dlc.par',
        'navimesh',
        'navimesh.par',
        'particle',
        'particle.par',
        'patch',
        'ps5',
        'puid.coyote',
        'reflection',
        'sddlc',
        'sddlc_en',
        'shader',
        'sound',
        'sound.par',
        'sound_en',
        'sound_en.par',
        'stage',
        'stage_common_coyote',
        'stage_coyote_ngen',
        'stmdlc',
        'stmdlc.par',
        'stmdlc_en',
        'stmdlc_en.par',
        'stream',
        'stream.par',
        'stream_en',
        'stream_en.par',
        'system',
        'talk_coyote',
        'talk_coyote.par',
        'ui.coyote.common',
        'ui.coyote.common.par',
        'ui.coyote.de',
        'ui.coyote.de.par',
        'ui.coyote.en',
        'ui.coyote.en.par',
        'ui.coyote.es',
        'ui.coyote.es.par',
        'ui.coyote.fr',
        'ui.coyote.fr.par',
        'ui.coyote.it',
        'ui.coyote.it.par',
        'ui.coyote.ja',
        'ui.coyote.ja.par',
        'ui.coyote.ko',
        'ui.coyote.ko.par',
        'ui.coyote.zh',
        'ui.coyote.zh.par',
        'ui.coyote.zhs',
        'ui.coyote.zhs.par',
        'version',
    }
