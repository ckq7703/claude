// Regenerates world-geo.js (land + country borders, Mercator-projected to a fixed box).
// Setup: npm i d3-geo@3.1.1 topojson-client@3.1.0
//        npm pack world-atlas@2.0.2 && tar xzf world-atlas-2.0.2.tgz   (creates ./package)
// Run:   node build-world-geo.mjs 50m     (or 110m for a smaller, coarser file)
import { geoMercator, geoPath, geoGraticule } from "d3-geo";
import * as topo from "topojson-client";
import fs from "fs";
const res = process.argv[2] || "50m";
const land = JSON.parse(fs.readFileSync(`package/land-${res}.json`));
const ctry = JSON.parse(fs.readFileSync(`package/countries-${res}.json`));
const W = 1000, LAT_N = 83, LAT_S = -60;
const p = geoMercator().scale(W / (2 * Math.PI)).translate([W / 2, 0]);
const yN = p([0, LAT_N])[1], yS = p([0, LAT_S])[1];
p.translate([W / 2, -yN]);
const H = Math.round(yS - yN);
p.clipExtent([[0, 0], [W, H]]);
const path = geoPath(p).digits(1);
const out = {
  W, H, k: +p.scale().toFixed(5), tx: +p.translate()[0].toFixed(4), ty: +p.translate()[1].toFixed(4),
  land: path(topo.feature(land, land.objects.land)),
  borders: path(topo.mesh(ctry, ctry.objects.countries, (a, b) => a !== b)),

};
const chk = p([105.85, 21.03]), lam = 105.85 * Math.PI / 180, phi = 21.03 * Math.PI / 180;
console.log(res, "H", H, "ratio", (W / H).toFixed(3), "sizes", out.land.length, out.borders.length);
console.log("d3", chk, "mine", [out.k * lam + out.tx, -out.k * Math.log(Math.tan(Math.PI / 4 + phi / 2)) + out.ty]);
fs.writeFileSync("world-geo.js", "/* Natural Earth (public domain) via world-atlas@2.0.2, Mercator-projected to a " + W + "x" + H + " box. Generated file. */\nwindow.WORLD_GEO=" + JSON.stringify(out) + ";\n");
