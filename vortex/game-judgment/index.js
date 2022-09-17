//Import some assets from Vortex we'll need.
const path = require('path');
const { fs, log, util } = require('vortex-api');

const GAME_ID = 'judgment';
const STEAMAPP_ID = '2058180';

const RMM_MODPAGE = 'https://github.com/SutandoTsukai181/RyuModManager/releases/latest';
const RMM_EXE = 'RyuModManager.exe';
const PARLESS_ASI = 'YakuzaParless.asi';
const DATA_PATH = path.join('runtime', 'media', 'data');
const MODS_PATH = path.join('runtime', 'media', 'mods');
const EXT_MODS_PATH = '_externalMods'
const GAME_EXE = path.join('runtime', 'media', 'Judgment.exe');

const tools = [
    {
      id: 'rmm',
      name: 'Run Ryu Mod Manager and launch the game',
      shortName: 'RMM',
      logo: 'rmm.png',
      executable: () => RMM_EXE,
      requiredFiles: [
        RMM_EXE,
        PARLESS_ASI,
      ],
      parameters: [
        '--run',
        '--silent',
      ],
      relative: true,
      shell: true,
    },
    {
        id: 'rmm',
        name: 'Run Ryu Mod Manager only',
        shortName: 'RMM',
        logo: 'rmm.png',
        executable: () => RMM_EXE,
        requiredFiles: [
          RMM_EXE,
          PARLESS_ASI,
        ],
        relative: true,
        shell: true,
      },
];

function main(context) {

    context.registerGame({
        id: GAME_ID,
        name: 'Judgment',
        mergeMods: true,
        queryPath: findGame,
        supportedTools: tools,
        queryModPath: () => MODS_PATH,
        logo: 'gameart.jpg',
        executable: () => GAME_EXE,
        requiredFiles: [
            GAME_EXE,
        ],
        setup: (discovery) => prepareForModding(discovery, context.api),
        environment: {
            SteamAPPId: STEAMAPP_ID,
        },
        details: {
            steamAppId: parseInt(STEAMAPP_ID),
        },
    });
    
    context.registerInstaller(
        'judgment-mod-installer',
        25,
        testMod,
        (files) => installMod(context.api, files)
    );
    
    return true
}

function findGame() {
    return util.GameStoreHelper.findByAppId([STEAMAPP_ID])
        .then(game => game.gamePath);
}

function prepareForModding(discovery, api) {
    return checkForRMM(api, path.join(discovery.path, 'runtime', 'media', RMM_EXE));
}

function checkForRMM(api, qModPath) {
    return fs.statAsync(qModPath)
      .catch(() => {
        api.sendNotification({
          id: 'rmm-missing',
          type: 'warning',
          title: 'RyuModManager not installed',
          message: 'You need to install RMM and run it at least once before modding the game.',
          actions: [
            {
              title: 'Get RMM',
              action: () => util.opn(RMM_MODPAGE).catch(() => undefined),
            }
          ]
        });
      });
}

function testMod(files, gameId) {
    // Leave the actual "testing" to installMod()
    return Promise.resolve({ supported: (gameId === GAME_ID), requiredFiles: [] });
}

async function installMod(api, files) {
    // Get the path to the game.
    const state = api.store.getState();
    const discovery = util.getSafe(state, ['settings', 'gameMode', 'discovered', GAME_ID], undefined);
    if (!discovery?.path) return Promise.reject(new util.ProcessCanceled('The game could not be discovered.'));

    const dataPath = path.join(discovery.path, DATA_PATH);

    // Find the root of the folder containing the modded files
    let rootPath = await findRootPath(files, dataPath);

    if (rootPath === '')
        return Promise.reject(new util.DataInvalid('Unrecognized or invalid mod. Manual installation is required.'));
    else if (rootPath === '.')
        rootPath = '';      // Fix root

    const idx = rootPath.length;
    let filtered = files.filter(file => (!file.endsWith(path.sep)) && (file.indexOf(rootPath) !== -1));

    const unsupported = findUnsupportedFiles(filtered);

    if (unsupported.length > 0) {
        api.sendNotification({
            id: 'yakuza-mod-unsupported-files',
            type: 'info',
            title: 'Mod may have unsupported files',
            message: 'This mod contains files that cannot be loaded by RMM. These files will not be copied to the mod folder, and will require manual installation.',
        });

        filtered = filtered.filter(file => (!unsupported.includes(file)));
    }

    // Check for other folders with modded files
    const otherPath = await findRootPath(files.filter(file => (file.indexOf(rootPath) === -1)), dataPath);

    if (otherPath !== '') {
        api.sendNotification({
            id: 'yakuza-mod-multiple-files',
            type: 'info',
            title: 'Mod may have additional files',
            message: 'This mod contains multiple folders with modded files. It may either have alternative options, or additional files that require manual installation.',
        });
    }
    
    return Promise.map(filtered, file => {
        return Promise.resolve({
            type: 'copy',
            source: file,
            destination: path.join(EXT_MODS_PATH, file.substr(idx)),
        });
    }).then(instructions => Promise.resolve({ instructions }));
}

async function findRootPath(files, dataPath) {
    // We expect this to stop very early, unless the mod is actually invalid
    for (let i = 0; i < files.length; i++)
    {
        let base = path.basename(files[i]);

        let found = false;

        await fs.statAsync(path.join(dataPath, base)).then(() => { found = true; }).catch(() => {});

        if (!found)
        {
            if (files[i].endsWith(path.sep)) {
                await fs.statAsync(path.join(dataPath, base + '.par')).then(() => { found = true; }).catch(() => { });
            }
        }

        if (found)
        {
            return Promise.resolve(path.dirname(files[i]));
        }
    }

    return Promise.resolve('');
}

function findUnsupportedFiles(files) {
    return [];
}

module.exports = {
    default: main,
};
