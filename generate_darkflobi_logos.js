const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');

// Create a 512x512 canvas
function createLogoCanvas() {
    return createCanvas(512, 512);
}

// Utility functions
function drawCircle(ctx, x, y, radius, fillStyle, strokeStyle = null, lineWidth = 2) {
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, 2 * Math.PI);
    ctx.fillStyle = fillStyle;
    ctx.fill();
    if (strokeStyle) {
        ctx.strokeStyle = strokeStyle;
        ctx.lineWidth = lineWidth;
        ctx.stroke();
    }
}

function drawEllipse(ctx, x, y, radiusX, radiusY, fillStyle, strokeStyle = null, lineWidth = 2) {
    ctx.beginPath();
    ctx.ellipse(x, y, radiusX, radiusY, 0, 0, 2 * Math.PI);
    ctx.fillStyle = fillStyle;
    ctx.fill();
    if (strokeStyle) {
        ctx.strokeStyle = strokeStyle;
        ctx.lineWidth = lineWidth;
        ctx.stroke();
    }
}

function drawGremlinBase(ctx) {
    // Background circle - dark but professional gradient
    const gradient = ctx.createRadialGradient(256, 256, 0, 256, 256, 256);
    gradient.addColorStop(0, '#2a1a4a');
    gradient.addColorStop(0.7, '#1a0d2e');
    gradient.addColorStop(1, '#0d0617');
    drawCircle(ctx, 256, 256, 256, gradient, '#4a2c6b', 6);

    // Gremlin head (main body) - friendly but mischievous
    drawEllipse(ctx, 256, 280, 85, 95, '#2d5a2d', '#1a3a1a', 4);
    
    // Gremlin ears - pointed and expressive
    drawEllipse(ctx, 195, 220, 28, 38, '#2d5a2d', '#1a3a1a', 3);
    drawEllipse(ctx, 317, 220, 28, 38, '#2d5a2d', '#1a3a1a', 3);
    
    // Inner ears
    drawEllipse(ctx, 195, 225, 15, 20, '#1a3a1a');
    drawEllipse(ctx, 317, 225, 15, 20, '#1a3a1a');

    // Eyes (large and expressive for the 😁)
    drawCircle(ctx, 225, 260, 22, '#ffffff', '#000', 3);
    drawCircle(ctx, 287, 260, 22, '#ffffff', '#000', 3);
    
    // Pupils with mischievous gleam
    drawCircle(ctx, 227, 262, 15, '#000');
    drawCircle(ctx, 289, 262, 15, '#000');
    drawCircle(ctx, 222, 257, 5, '#ffffff');
    drawCircle(ctx, 284, 257, 5, '#ffffff');

    // Nose - small and cute
    drawEllipse(ctx, 256, 290, 10, 15, '#1a3a1a');

    // The signature BIG grin 😁 
    ctx.beginPath();
    ctx.arc(256, 305, 40, 0.15 * Math.PI, 0.85 * Math.PI);
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 5;
    ctx.stroke();
    
    // Teeth for the grin - making it really happy
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#ccc';
    ctx.lineWidth = 1;
    for (let i = 0; i < 8; i++) {
        const x = 230 + i * 7;
        const y = 325;
        ctx.fillRect(x, y, 5, 10);
        ctx.strokeRect(x, y, 5, 10);
    }

    // Gremlin shoulders/arms
    drawEllipse(ctx, 180, 350, 30, 50, '#2d5a2d', '#1a3a1a', 3);
    drawEllipse(ctx, 332, 350, 30, 50, '#2d5a2d', '#1a3a1a', 3);

    return ctx;
}

function drawCrown(ctx) {
    // Professional crown with CEO vibes
    const crownBase = 190;
    const crownTop = 165;
    const crownWidth = 132;
    
    // Crown base - solid gold
    const goldGradient = ctx.createLinearGradient(crownBase, crownTop + 20, crownBase, crownTop + 40);
    goldGradient.addColorStop(0, '#ffd700');
    goldGradient.addColorStop(1, '#b8860b');
    
    ctx.fillStyle = goldGradient;
    ctx.fillRect(crownBase, crownTop + 30, crownWidth, 18);
    
    // Crown points - more regal
    ctx.beginPath();
    ctx.moveTo(crownBase, crownTop + 30);
    ctx.lineTo(crownBase + 25, crownTop - 5);
    ctx.lineTo(crownBase + 40, crownTop + 20);
    ctx.lineTo(crownBase + 66, crownTop - 15); // Center tallest
    ctx.lineTo(crownBase + 92, crownTop + 20);
    ctx.lineTo(crownBase + 107, crownTop - 5);
    ctx.lineTo(crownBase + 132, crownTop + 30);
    ctx.closePath();
    ctx.fillStyle = goldGradient;
    ctx.fill();
    
    // Crown jewels - executive level bling
    drawCircle(ctx, crownBase + 66, crownTop + 5, 10, '#ff2244'); // Ruby center
    drawCircle(ctx, crownBase + 35, crownTop + 10, 6, '#22ff44'); // Emerald
    drawCircle(ctx, crownBase + 97, crownTop + 10, 6, '#2244ff'); // Sapphire
    
    // Crown outline for definition
    ctx.strokeStyle = '#996600';
    ctx.lineWidth = 3;
    ctx.stroke();
}

function drawBusinessSuit(ctx) {
    // Executive suit jacket
    ctx.beginPath();
    ctx.moveTo(210, 360);
    ctx.lineTo(235, 335);
    ctx.lineTo(256, 345);
    ctx.lineTo(277, 335);
    ctx.lineTo(302, 360);
    ctx.lineTo(290, 400);
    ctx.lineTo(222, 400);
    ctx.closePath();
    ctx.fillStyle = '#0a0a0a';
    ctx.fill();
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Dress shirt collar
    ctx.beginPath();
    ctx.moveTo(240, 345);
    ctx.lineTo(256, 340);
    ctx.lineTo(272, 345);
    ctx.lineTo(268, 365);
    ctx.lineTo(244, 365);
    ctx.closePath();
    ctx.fillStyle = '#ffffff';
    ctx.fill();

    // Power tie - deep purple for DARK aesthetic
    ctx.beginPath();
    ctx.moveTo(256, 345);
    ctx.lineTo(246, 395);
    ctx.lineTo(266, 395);
    ctx.closePath();
    ctx.fillStyle = '#4a0e4e';
    ctx.fill();
    ctx.strokeStyle = '#2a0e2e';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Tie pattern - subtle executive stripes
    ctx.strokeStyle = '#6a2e6e';
    ctx.lineWidth = 1.5;
    for (let i = 0; i < 4; i++) {
        const y = 355 + i * 12;
        ctx.beginPath();
        ctx.moveTo(248, y);
        ctx.lineTo(264, y);
        ctx.stroke();
    }

    // Suit buttons
    drawCircle(ctx, 240, 375, 3, '#333');
    drawCircle(ctx, 272, 375, 3, '#333');
}

function addBrandText(ctx, subtitle = '') {
    // Main brand text - bold and clean
    ctx.font = 'bold 28px Arial, sans-serif';
    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 2;
    ctx.textAlign = 'center';
    ctx.strokeText('DARKFLOBI', 256, 460);
    ctx.fillText('DARKFLOBI', 256, 460);
    
    // Subtitle if provided
    if (subtitle) {
        ctx.font = 'bold 16px Arial, sans-serif';
        ctx.fillStyle = '#cccccc';
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 1;
        ctx.strokeText(subtitle, 256, 485);
        ctx.fillText(subtitle, 256, 485);
    }
}

// Generate Logo Variation 1: Crown Gremlin
function generateCrownLogo() {
    const canvas = createLogoCanvas();
    const ctx = canvas.getContext('2d');
    
    drawGremlinBase(ctx);
    drawCrown(ctx);
    addBrandText(ctx, 'EMPEROR');
    
    return canvas;
}

// Generate Logo Variation 2: Business Suit Gremlin  
function generateSuitLogo() {
    const canvas = createLogoCanvas();
    const ctx = canvas.getContext('2d');
    
    drawGremlinBase(ctx);
    drawBusinessSuit(ctx);
    addBrandText(ctx, 'CEO');
    
    return canvas;
}

// Generate Logo Variation 3: CEO Emperor (Crown + Suit)
function generateEmperorLogo() {
    const canvas = createLogoCanvas();
    const ctx = canvas.getContext('2d');
    
    drawGremlinBase(ctx);
    drawBusinessSuit(ctx);
    drawCrown(ctx);
    addBrandText(ctx, 'EMPIRE');
    
    return canvas;
}

// Generate all three variations
async function generateAllLogos() {
    try {
        console.log('Generating DARKFLOBI logos...');
        
        // Generate all three variations
        const crownLogo = generateCrownLogo();
        const suitLogo = generateSuitLogo(); 
        const emperorLogo = generateEmperorLogo();
        
        // Save as high-quality PNG files
        const buffer1 = crownLogo.toBuffer('image/png');
        const buffer2 = suitLogo.toBuffer('image/png');
        const buffer3 = emperorLogo.toBuffer('image/png');
        
        fs.writeFileSync('darkflobi_emperor.png', buffer1);
        fs.writeFileSync('darkflobi_ceo.png', buffer2);
        fs.writeFileSync('darkflobi_empire.png', buffer3);
        
        console.log('✅ Successfully generated 3 logo variations:');
        console.log('   - darkflobi_emperor.png (Crown version)');
        console.log('   - darkflobi_ceo.png (Business suit version)');  
        console.log('   - darkflobi_empire.png (Crown + Suit combo)');
        console.log('');
        console.log('All logos are 512x512 PNG format, ready for token listings!');
        
    } catch (error) {
        console.error('Error generating logos:', error.message);
    }
}

// Run the generator
generateAllLogos();