import cairo
import rsvg

def convert(data, ofile, maxwidth=0, maxheight=0):

    svg = rsvg.Handle(data=data)

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
    surface.write_to_png(ofile)