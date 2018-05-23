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
* A bitmap editor is available at <http://www.nand2tetris.org/projects/09/BitmapEditor/BitmapEditor.html>, which can be used to create customized sprite.
* Syntax highlighting for Jack in Sublime text:
  * https://github.com/swarn/sublime-jack
  * https://www.sublimetext.com/docs/3/scope_naming.html

