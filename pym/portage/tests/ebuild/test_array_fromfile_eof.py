# Copyright 2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Id$

import array
import tempfile

from portage import _unicode_decode
from portage import _unicode_encode
from portage.tests import TestCase

class ArrayFromfileEofTestCase(TestCase):

	def testArrayFromfileEof(self):
		# This tests if the following python issue is fixed
		# in the currently running version of python:
		#   http://bugs.python.org/issue5334

		input_data = "an arbitrary string"
		input_bytes = _unicode_encode(input_data,
			encoding='utf_8', errors='strict')
		f = tempfile.TemporaryFile()
		f.write(input_bytes)

		f.seek(0)
		data = []
		eof = False
		while not eof:
			a = array.array('B')
			try:
				a.fromfile(f, len(input_bytes) + 1)
			except EOFError:
				# python-3.0 lost data here
				eof = True

			if not a:
				eof = True
			else:
				data.append(_unicode_decode(a.tostring(),
					encoding='utf_8', errors='strict'))

		f.close()

		self.assertEqual(input_data, ''.join(data))
