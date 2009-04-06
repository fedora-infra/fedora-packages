from glob import glob
from os import walk
from os.path import join

from xml.parsers import expat 
def rec_glob(top_dir, pattern):
    files = []
    for (dirpath, dirnames, filenames) in walk(top_dir):
        files.extend(glob(join(dirpath, pattern)))

    return files

class sax_callbacks:
    def startDocument(self):
        self.el_stack = []

    def endDocument(self):
        if len(self.el_stack) > 0:
            raise Exception('Error: tags not closed %s', str(self.el_stack))

    def startElement(self, tag, attrs):
        self.el_stack.append(tag)        

    def endElement(self, tag):
        last_tag = self.el_stack.pop()
        if tag != last_tag:
            raise Exception('Error: mismatched tags (last_tage: %s, closing_tag: %s)', last_tag, tag)

error_files = []
for mak_file in rec_glob('.', '*.mak'):
    f = open(mak_file, 'r')
    buf = f.read()
    f.close()
    
    handler = sax_callbacks()

    try:
        ctxt = expat.ParserCreate()
        handler.startDocument()
        ctxt.StartElementHandler = handler.startElement
        ctxt.EndElementHandler = handler.endElement
        ctxt.Parse(buf, 1)
        handler.endDocument()

    except Exception, e:
        if expat.ErrorString(e.code) != expat.errors.XML_ERROR_UNDEFINED_ENTITY:
            print "Parsing " + mak_file + " failed"
            print e
        
