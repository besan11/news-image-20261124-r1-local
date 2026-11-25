// Entry program for news-image-20261124 (Node 22, standard library only).
// The front page itself is entry.png, drawn in this repository by render.py.
// This program only copies that finished image into the grader's output
// folder. It uses no network, writes nothing else, and never deletes the
// output directory.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The copy is byte-for-byte, so two runs always produce identical output.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
