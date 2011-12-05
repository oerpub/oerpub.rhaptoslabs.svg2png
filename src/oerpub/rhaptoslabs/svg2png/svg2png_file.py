'''
Author: Marvin Reimer
Copyright (C) 2011 Katherine Fletcher.
Funding was provided by The Shuttleworth Foundation as part of the
OER Roadmap Project.

If the license this software is distributed under is not suitable
for your purposes, you may contact the copyright holder through
oer-roadmap-discuss@googlegroups.com to discuss different licensing
terms.

This file is part of oerpub.rhaptoslabs.svg2png

oerpub.rhaptoslabs.svg2png is free software: you can
redistribute it and/or modify it under the terms of the GNU Lesser
General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

oerpub.rhaptoslabs.svg2png is distributed in the hope that it
will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with oerpub.rhaptoslabs.svg2png.
If not, see <http://www.gnu.org/licenses/>.
'''

import os
import glob
import cairo
import rsvg

current_dir = os.path.dirname(__file__)
TESTBED_INPUT_DIR = os.path.join(current_dir, 'input_svg_samples')  # the testbed folder with some svg files inside
TESTBED_INPUT_FILEEXT = "*.svg"
TESTBED_OUTPUT_DIR = os.path.join(current_dir, 'output_png_samples')

# converts svg binary data to a png file
def svg2png_file(svg_data, png_filename, maxwidth=0, maxheight=0):

    svg = rsvg.Handle(data=svg_data)

    x = width = svg.props.width
    y = height = svg.props.height
    print "actual dims are " + str((width, height))
    print "converting to " + str((maxwidth, maxheight))

    yscale = xscale = 1

    if (maxheight != 0 and width > maxwidth) or (maxheight != 0 and height > maxheight):
        x = maxwidth
        y = float(maxwidth)/float(width) * height
        print "first resize: " + str((x, y))
        if y > maxheight:
            y = maxheight
            x = float(maxheight)/float(height) * width
            print "second resize: " + str((x, y))
        xscale = float(x)/svg.props.width
        yscale = float(y)/svg.props.height

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, x, y)
    context = cairo.Context(surface)
    context.scale(xscale, yscale)
    svg.render_cairo(context)
    surface.write_to_png(png_filename)

# opens svg file and save png 
def svg_file2png_file(svg_filename, png_filename):
    svg_file = open(svg_filename)
    svg_data = svg_file.read()
    svg2png_file(svg_data, png_filename)

# prints a status message surrounded by some lines
def print_status(status_message):
    print '=' * 79
    print status_message
    print '=' * 79

# process the svg testbed and convert the files to png
def test_svg2png():
    for svg_filename in glob.glob(os.path.join(TESTBED_INPUT_DIR, TESTBED_INPUT_FILEEXT)):
        # output filename string preparation
        just_filename = os.path.basename(svg_filename)
        just_filename_no_ext = os.path.splitext(just_filename)[0]
        png_filename = os.path.join(TESTBED_OUTPUT_DIR, just_filename_no_ext + '.png')

        print_status('Convert SVG to PNG: %s' % just_filename)
        svg_file2png_file(svg_filename, png_filename)

if __name__ == "__main__":
    test_svg2png()

