class Model:
    ESBUILD = """const fs = require('fs');
const pug = require('pug');

if (process.argv.length > 2) {
    let errors = [];
    for (let i = 2 ; i < process.argv.length ; i++) {
        const target = process.argv[i];
        const [sourceTarget, outputTarget] = target.split('::');
        const targetpath = sourceTarget + '.pug';
        const savepath = (outputTarget || sourceTarget) + '.html';
        try {
            const compiledFunction = pug.compileFile(targetpath);
            const html = compiledFunction();
            let shouldWrite = true;
            if (fs.existsSync(savepath)) {
                shouldWrite = fs.readFileSync(savepath, 'utf8') !== html;
            }
            if (shouldWrite) {
                fs.writeFileSync(savepath, html, "utf8")
            }
        } catch (e) {
            errors.push({ file: targetpath, error: e.message });
            console.error('[PUG ERROR] ' + targetpath + ': ' + e.message);
        }
    }
    if (errors.length > 0) {
        console.error('[PUG BUILD] ' + errors.length + ' file(s) failed to compile:');
        errors.forEach(e => console.error('  - ' + e.file));
    }
} else {
    console.log('[WIZ BUILD] Angular build is executed directly by builder.py');
    process.exit(0);
}"""

    ENV = """export const environment = {
    production: true
};"""

    TSCONFIG = """{
    "compileOnSave": false,
    "compilerOptions": {
        "baseUrl": "./",
        "outDir": "./dist/out-tsc",
        "forceConsistentCasingInFileNames": true,
        "strict": false,
        "noImplicitOverride": false,
        "noPropertyAccessFromIndexSignature": false,
        "noImplicitReturns": false,
        "noFallthroughCasesInSwitch": false,
        "skipLibCheck": true,
        "allowJs": true,
        "checkJs": false,
        "sourceMap": true,
        "declaration": false,
        "downlevelIteration": true,
        "experimentalDecorators": true,
        "moduleResolution": "node",
        "importHelpers": true,
        "target": "ES2022",
        "module": "ES2022",
        "useDefineForClassFields": false,
        "lib": [
            "ES2022",
            "dom"
        ]
    },
    "angularCompilerOptions": {
        "enableI18nLegacyMessageIdFormat": false,
        "strictInjectionParameters": false,
        "strictInputAccessModifiers": false,
        "strictTemplates": false
    }
}"""

    STYLES = '@use "styles/styles";'

    POSTCSS = """{
    \"plugins\": {
        \"@tailwindcss/postcss\": {}
    }
}"""

    TAILWINDCSS = """@import \"tailwindcss\";
@config \"./tailwind.config.js\";
"""

    TAILWIND = """/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{html,ts}",
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}"""