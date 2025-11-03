
* { box-sizing: border-box; font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif; }
body { margin: 0; background: #0f0f12; color: #f2f2f2; }
header { padding: 24px 16px; text-align: center; background: #15151a; border-bottom: 1px solid #2a2a33; }
header h1 { margin: 0 0 8px 0; }
main { max-width: 980px; margin: 0 auto; padding: 16px; display: grid; gap: 16px; }
.card { background: #15151a; border: 1px solid #2a2a33; border-radius: 12px; padding: 16px; }
.row { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }
.inputs { display: flex; gap: 8px; flex-wrap: wrap; }
input { width: 80px; padding: 8px; border-radius: 8px; border: 1px solid #444; background: #1b1b20; color: #fff; text-align: center; }
.hint { color: #bdbdc7; font-size: 0.9rem; margin: 6px 0 0; }
.buttons { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
button { background: #7c3aed; border: none; padding: 10px 14px; border-radius: 8px; color: #fff; cursor: pointer; }
button:hover { background: #9f67ff; }
button.secondary { background: #2d2d35; }
button.secondary:hover { background: #3a3a44; }
#passos { white-space: pre-wrap; background: #101015; border: 1px solid #2a2a33; border-radius: 8px; padding: 12px; }
#grafico { width: 100%; height: 520px; }
.legend-hint { margin-top: 8px; color: #bdbdc7; font-size: 0.9rem; }
