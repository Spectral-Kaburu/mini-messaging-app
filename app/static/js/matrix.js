const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

// ────────────────────────────────────────────────
//  Settings – tweak these to control overflow amount
// ────────────────────────────────────────────────
const OVERFLOW_PCT = 0.10;           // 10% extra on left/right/bottom
const fontSize = 16;
const letters = "WelcomeToChatApp01$+-=.:, ";   // added some extras for better rain feel

// ────────────────────────────────────────────────
// Calculate extended (overflow) dimensions
// ────────────────────────────────────────────────
function resizeCanvas() {
    const w = window.innerWidth;
    const h = window.innerHeight;

    // We want ~10% more width and 10% more height at bottom
    canvas.width  = Math.ceil(w * (1 + OVERFLOW_PCT * 2));   // +10% left + 10% right
    canvas.height = Math.ceil(h * (1 + OVERFLOW_PCT));       // only +10% at bottom

    // Shift drawing origin so left overflow is hidden
    // → we translate the context left by 10% of screen width
    ctx.setTransform(1, 0, 0, 1, -w * OVERFLOW_PCT, 0);
}

resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// ────────────────────────────────────────────────
const columns = Math.ceil(canvas.width / fontSize);
const drops = new Array(columns).fill(1);   // start above top

function draw() {
    // semi-transparent black fade
    ctx.fillStyle = "rgba(0,0,0,0.05)";
    ctx.fillRect(-canvas.width, 0, canvas.width * 3, canvas.height); // wide clear

    ctx.fillStyle = "#F00";   // classic matrix green (or keep #F00 if you prefer red)
    ctx.font = `${fontSize}px monospace`;

    drops.forEach((y, i) => {
        const text = letters[Math.floor(Math.random() * letters.length)];
        
        // x position includes the left overflow shift
        const x = i * fontSize;
        ctx.fillText(text, x, y * fontSize);

        // reset when gone far enough past bottom
        if (y * fontSize > canvas.height + fontSize * 5) {
            if (Math.random() > 0.975) {
                drops[i] = 0;           // occasional fast reset
            }
        }
        drops[i] += 0.5 + Math.random() * 0.4;   // slight speed variation looks nicer
    });
}

setInterval(draw, 33);

/*const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.width = window.innerWidth;
canvas.height = window.innerHeight; // to cover fullscreen too, figure out a less "juakali" way

const letters = "WelcomeToChatApp";
const fontSize = 16;
const columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function draw() {
ctx.fillStyle = "rgba(0,0,0,0.05)";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.fillStyle = "#F00";
ctx.font = fontSize + "px monospace";

drops.forEach((y, i) => {
    const text = letters[Math.floor(Math.random() * letters.length)];
    ctx.fillText(text, i * fontSize, y * fontSize);
    drops[i] = y * fontSize > canvas.height + 10 && Math.random() > 0.975 ? 0 : y + 0.5;
});
}

setInterval(draw, 33);*/