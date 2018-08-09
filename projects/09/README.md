## Project 09

Implement an application in Jack high-level language.

In my case, the app is called `Adventure`. So far it only creates an avatar that can move around.

### Getting started
All source files (i.e., `*.jack`) are put in one directory, whose name is the app name (e.g., `Adventure`).

**Step 1:** compile all `*.jack` files into `*.vm` files.
```bash
$ ../../tools/JackCompiler.[sh|bat] Adventure
```
Or use [when-changed](https://github.com/joh/when-changed):
```bash
# on windows
$ when-changed -v Adventure/*.jack -c F:\\course\\Nand2Tetris\\tools\\JackCompiler.bat Adventure
# on linux
$ when-changed -v Adventure/*.jack -c ../../tools/JackCompiler.sh Adventure
```
**Step 2:** start `VMEmulator`. Load the **whole directory** (say Adventure) containing all `*.vm` files (not a single `vm` file). Turn off animation for graphic app, otherwise we have to wait for a long time to see stuff on the screen.
```bash
$ ../../tools/VMEmulator.[sh|bat]
```

### Notes
* More sample Jack apps (e.g., `Pong`) can be found in `./projects/11`. They are given as test cases for Jack compiler but can be re-purposed as samples.
* A bitmap editor is available at <https://arieljannai.gitlab.io/Nand2TetrisBitmapEditor/>, which can be used to create customized sprite.
* Screen and MemoryAddress: mentioned in `Adventure/Avatar.jack - draw()`, copied here
```jack
// each memory addr stores 16-bit value, namely 16 pixels (only white and black)
// for example, memAddr=16384 represents the first 16 pixels (x=0..15, y=0)
// memAddr=16385 represents the next 16 pixels (x=16..31, y=0)
// for the screen with width of 512 pixels, we have 512/16 = 32
// namely, if we go to next line (y + 1) with the same x, we have to use (memAddr+32)
```
* Syntax highlighting for Jack in Sublime text:
  * https://github.com/swarn/sublime-jack
  * https://www.sublimetext.com/docs/3/scope_naming.html

