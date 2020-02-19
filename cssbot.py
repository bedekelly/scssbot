import os
import subprocess
import tempfile
import shlex

import sass

default_page = """
<html>
<head>
<style>

html,body {{
  margin: 0;
  padding: 0;
}}

body {{
  background: black;
  width: 512px;
  height: 512px;
}}

.parent {{
  width: 100vw;
  height: 100vh;
  display: grid;
  place-items: center;
}}

{styles}
</style>
<head>
<body>

<div class="parent">
    <div class="r"></div>
</div>

</body>
</html>
"""

local = False
browserCommand = '"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"' if local else "chromium-browser"
command_template = (
    '%s {headless} --screenshot={output_filename} --no-sandbox '
    "--hide-scrollbars --window-size=512,512 --default-background-color=0 {filename}"
) % browserCommand


def compile_styles(raw_scss):
    return sass.compile(string=raw_scss)


def take_screenshot(raw_styles, debug=False):
    wrapped_styles = f".r {{ width: 100%; height: 100%; {raw_styles}}}"
    compiled_styles = compile_styles(wrapped_styles)
    rendered_html = default_page.format(styles=compiled_styles)

    with tempfile.NamedTemporaryFile("r+", suffix=".html", buffering=1) as file:
        file.write(rendered_html)
        output = os.path.basename(file.name).replace(".html", ".png")
        command = command_template.format(
            filename=file.name,
            output_filename=f"./{output}",
            headless="--headless" if not debug else "",
        )
        subprocess.call(shlex.split(command), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return f"./{output}"


test_thing = """
    background: pink;
    width: 50px;
    height: 50px;
    margin: 0 auto;
    position: relative;
    display: grid;
    place-items: center;
    
    &:before {
        background: blue;
        width: 10px;
        height: 10px;
        display: block;
        content: '';
    }
"""

if __name__ == "__main__":
    take_screenshot(test_thing, debug=True)
