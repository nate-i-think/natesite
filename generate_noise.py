"""
Generate a tileable noise texture for CRT dithering effect.
Creates a subtle grayscale noise PNG that tiles seamlessly.
"""

import random

def generate_noise_png(filename, size=64):
    """
    Generate a grayscale noise PNG without external dependencies.
    Uses raw PNG encoding with zlib compression.
    """
    import zlib
    import struct

    width = height = size

    # Generate noise pixels - subtle variation around middle gray
    # We want low-contrast noise so it's not visually distracting
    pixels = []
    for y in range(height):
        row = [0]  # PNG filter byte (0 = no filter)
        for x in range(width):
            # Random value 0-255, but we'll use alpha channel for subtlety
            # White noise with varying alpha works better than gray noise
            noise_val = random.randint(0, 255)
            row.append(noise_val)  # grayscale value
        pixels.append(bytes(row))

    raw_data = b''.join(pixels)

    def png_chunk(chunk_type, data):
        """Create a PNG chunk with CRC."""
        chunk = chunk_type + data
        crc = zlib.crc32(chunk) & 0xffffffff
        return struct.pack('>I', len(data)) + chunk + struct.pack('>I', crc)

    # PNG signature
    png_signature = b'\x89PNG\r\n\x1a\n'

    # IHDR chunk (image header)
    # Width, Height, Bit depth (8), Color type (0=grayscale), Compression, Filter, Interlace
    ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 0, 0, 0, 0)
    ihdr = png_chunk(b'IHDR', ihdr_data)

    # IDAT chunk (compressed image data)
    compressed = zlib.compress(raw_data, 9)
    idat = png_chunk(b'IDAT', compressed)

    # IEND chunk (image end)
    iend = png_chunk(b'IEND', b'')

    # Write the PNG file
    with open(filename, 'wb') as f:
        f.write(png_signature + ihdr + idat + iend)

    print(f"Generated {filename} ({width}x{height} grayscale noise)")

if __name__ == '__main__':
    generate_noise_png('assets/img/noise.png', size=64)
