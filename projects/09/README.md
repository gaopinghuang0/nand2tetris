## Project 09

Implement an application of my choice in Jack high-level language.

### Getting started
All files (i.e., `*.jack`) are put in one directory, whose name is the app name (e.g., `MyApp`)
```bash
$ ../../tools/JackCompiler MyApp
$ ../../tools/VMEmulator
```
Then load the whole directory (say MyApp) and run. Do not go inside the directory and load a single file. Turn off animation for graphic app, otherwise we have to wait for a long time to see stuff on the screen.

### Notes
* More sample Jack apps (e.g., `Pong`) can be found in `./projects/11`. They are given as test cases for Jack compiler and thus can be treated as samples.
* A bitmap editor is available at <http://www.nand2tetris.org/projects/09/BitmapEditor/BitmapEditor.html>, which can be used to create customized sprite.
* Syntax highlighting for Jack in sublime text:
  * https://github.com/swarn/sublime-jack
  * https://www.sublimetext.com/docs/3/scope_naming.html
* Use `when-changed`:
```bash
$ when-changed -v Pong/*.jack -c F:\\course\\Nand2Tetris\\tools\\JackCompiler.bat Pong
```
