const { createCanvas } = require('canvas')
const fs = require('fs')
const path = require('path')

const sizes = [192, 512]
const outDir = path.join(__dirname, 'app', 'public', 'icons')

if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true })

for (const size of sizes) {
  const canvas = createCanvas(size, size)
  const ctx = canvas.getContext('2d')

  // Background
  ctx.fillStyle = '#7c3aed'
  ctx.fillRect(0, 0, size, size)

  // Text "LS"
  const fontSize = size * 0.4
  ctx.fillStyle = '#ffffff'
  ctx.font = `bold ${fontSize}px sans-serif`
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText('LS', size / 2, size / 2)

  const buf = canvas.toBuffer('image/png')
  fs.writeFileSync(path.join(outDir, `icon-${size}x${size}.png`), buf)
  console.log(`Generated icon-${size}x${size}.png`)
}

// Maskable icon (with padding)
const maskSize = 512
const canvas = createCanvas(maskSize, maskSize)
const ctx = canvas.getContext('2d')
ctx.fillStyle = '#7c3aed'
ctx.fillRect(0, 0, maskSize, maskSize)
const fontSize = maskSize * 0.3
ctx.fillStyle = '#ffffff'
ctx.font = `bold ${fontSize}px sans-serif`
ctx.textAlign = 'center'
ctx.textBaseline = 'middle'
ctx.fillText('LS', maskSize / 2, maskSize / 2)
const buf = canvas.toBuffer('image/png')
fs.writeFileSync(path.join(outDir, 'icon-maskable-512x512.png'), buf)
console.log('Generated icon-maskable-512x512.png')
