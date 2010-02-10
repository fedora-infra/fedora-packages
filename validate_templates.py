# This file is part of Fedora Community.
# Copyright (C) 2008-2010  Red Hat, Inc.
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
        
