from .core import Component, Namespace
import re
# required for the Component pack
# packname is the name of the module/package to be used
# packtype tells the extension that this is in fact a Component Pack, not a different type of package
# packversion specifies the version of this module/package
# packdeps is a list of external dependancies required for the module/package

__packname__ = 'base'

__packtype__ = 'Component Pack'

__packversion__ = "1.0"

__packdeps__ = []

# Component to put css in the head
# can take a string, wich will be evaluated as the css of a style tag
# can also take css kwarg which also will be evaluated as the css of a style tag
# can take url kwarg which will specify the url of a link tag with rel="stylesheet"
class CssComponent(Component):
    """Component to put CSS in the head
    can take a string, which will be evaluated as the css of a style tag.
    Can take `css` kwarg instead, which also will be evaluated as the css of a style tag.
    Can take `url` kwarg instead, which will specify the url of a link tag with `rel="stylesheet`"
    """
    class _Parser(): # parser to minify css
        def __init__(self, css):
            self.css = css
        def __call__(self, css=None):
            if css == None: #set default param
                css = self.css
            minifiedCss = re.sub(r"\/\*.*?\*\/","", css) #remove comments
            minifiedCss = re.sub(r"\n","", minifiedCss) # remove newlines
            minifiedCss = re.sub(r"[\t\ ]{2,}|\t"," ", minifiedCss) # collapse spaces
            #TODO: update with regex
            temp = css.split('{')
            temp = [t.split("}") for t in temp]
            ret = temp
            for i, j in enumerate(temp):
                if ":" in j:
                    ret[i] = j.replace(" ", "")
            return ret

    def __html__(self, *args, **kwargs):
        def minify_css(css):
            minifiedCss = re.sub(r"\/\*.*?\*\/","", css) #remove comments
            minifiedCss = re.sub(r"\n","", minifiedCss) # remove newlines
            minifiedCss = re.sub(r"[\t\ ]{2,}|\t"," ", minifiedCss) # collapse spaces
            print("repr: " + repr(minifiedCss))
            return minifiedCss
        minifycss = self.kwargs.get('minify') or False
        if (url := self.kwargs.get('url')) is not None:
            return '<link href="' + url + '" rel="stylesheet"></link>'
        if (css := kwargs.get('css')) is not None:
            if minifycss:
                return '<style>' + minify_css(css) + '</style>'
            else:
                return '<style>' + css + '</style>'
        try:
            if (instargs := self.args[0] ) is not None and isinstance(instargs, str):
                if minifycss:
                    return '<style>' + minify_css(str(self.args[0])) + '</style>'
                else:
                    return '<style>' +str(self.args[0]) + '</style>'
            elif len(instargs):
                innercss = ""
                for cls in instargs:
                    if cls is not CssComponent and isinstance(type, cls):
                        innercss += cls().__css__()
                if minifycss:
                    return "<style>" + minify_css(innercss) + "</style>"
                else:
                    return "<style>" + innercss + "</style>"
        except Exception as e:
            print(e)
class JsComponent(Component):
    """Component to put insert Javascript.
    can take a string, which will be evaluated as the js of a script tag.
    """
    # TODO: Implement JS component
    def __html__(self, *args, **kwargs):
        def minify_js(js):
            return js
        minifyjs = self.kwargs.get('minify') or False
        if (url := self.kwargs.get('url')) is not None:
            return '<script src="' + url + '"></script>'
        if (js := self.kwargs.get('js')) is not None:
            if minifyjs:
                return '<script>' + minify_js(js) + '</script>'
            else:
                return '<script>' + js + '</script>'
        try:
            if (instargs := self.args[0] ) is not None and isinstance(instargs, str):
                if minifycss:
                    return '<script>' + minify_css(str(self.args[0])) + '</script>'
                else:
                    return '<script>' +str(self.args[0]) + '</script>'
            elif len(instargs):
                innerjs = ""
                for cls in instargs:
                    if cls is not JsComponent and isinstance(type, cls):
                        innerjs += cls().__js__()
                if minifycss:
                    return "<script>" + minify_js(innerjs) + "</style>"
                else:
                    return "<script>" + innerjs + "</script>"
        except Exception as e:
            print(e)
css = CssComponent("""
.test {
    color: red;
    float: right;
}
.test:hover {
    color: green;
}
.test::after { /* set after content */
    content: "Hello World";
}
@media print {
    .test {
        color: black;
    }
}
@media only screen and (max-width: 600px) {
    .test {
        float: none;
        width: 100%;
    }
}
""", minify=True)
js = JsComponent(__components__)


