import game
import asyncio


async def main():
    g = game.Game()

    g.running = True
    while g.running:
        g.update()
        await asyncio.sleep(0)

        g.render()

asyncio.run( main() )
