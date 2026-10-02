import { writeFileSync, mkdirSync, existsSync } from 'fs'
import { join } from 'path'
import { deflateSync } from 'zlib'

function createPNG(width, height, r, g, b) {
  const raw = []
  for (let y = 0; y < height; y++) {
    raw.push(0) // filter none
    for (let x = 0; x < width; x++) {
      raw.push(r, g, b, 255)
    }
  }
  const compressed = deflateSync(Buffer.from(raw))

  function chunk(type, data) {
    const len = Buffer.alloc(4)
    len.writeUInt32BE(data.length)
    const typeData = Buffer.concat([Buffer.from(type), data])
    const crc = crc32(typeData)
    const crcBuf = Buffer.alloc(4)
    crcBuf.writeUInt32BE(crc >>> 0)
    return Buffer.concat([len, typeData, crcBuf])
  }

  function crc32(buf) {
    let c = 0xffffffff
    for (let i = 0; i < buf.length; i++) {
      c ^= buf[i]
      for (let j = 0; j < 8; j++) {
        c = (c >>> 1) ^ (c & 1 ? 0xedb88320 : 0)
      }
    }
    return c ^ 0xffffffff
  }

  const ihdr = Buffer.alloc(13)
  ihdr.writeUInt32BE(width, 0)
  ihdr.writeUInt32BE(height, 4)
  ihdr[8] = 8 // bit depth
  ihdr[9] = 2 // color type RGB
  ihdr[10] = 0 // compression
  ihdr[11] = 0 // filter
  ihdr[12] = 0 // interlace

  return Buffer.concat([
    Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), // PNG signature
    chunk('IHDR', ihdr),
    chunk('IDAT', compressed),
    chunk('IEND', Buffer.alloc(0))
  ])
}

const outDir = join(process.cwd(), 'app', 'public', 'icons')
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true })

// Purple background: #7c3aed = rgb(124, 58, 237)
const sizes = [192, 512]
for (const size of sizes) {
  const png = createPNG(size, size, 124, 58, 237)
  writeFileSync(join(outDir, `icon-${size}x${size}.png`), png)
  console.log(`icon-${size}x${size}.png`)
}
const mask = createPNG(512, 512, 124, 58, 237)
writeFileSync(join(outDir, 'icon-maskable-512x512.png'), mask)
console.log('icon-maskable-512x512.png')
