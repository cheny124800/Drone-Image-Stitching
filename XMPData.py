from PIL import Image
import xmltodict

def xmp(filename):

    with Image.open(filename) as im:
        for segment, content in im.applist:

            marker, body = content.split(b'\x00', 1)

            if segment == 'APP1' and marker == b'http://ns.adobe.com/xap/1.0/':
                # parse the XML string with any method you like
                dji = xmltodict.parse(body)
                '''for key, values in dji['x:xmpmeta']['rdf:RDF']['rdf:Description'].items():
                    print (key + " " + values)
                '''

                alt = dji['x:xmpmeta']['rdf:RDF']['rdf:Description']['@drone-dji:AbsoluteAltitude']
                roll = dji['x:xmpmeta']['rdf:RDF']['rdf:Description']['@drone-dji:FlightRollDegree']
                yaw = dji['x:xmpmeta']['rdf:RDF']['rdf:Description']['@drone-dji:FlightYawDegree']
                pitch = dji['x:xmpmeta']['rdf:RDF']['rdf:Description']['@drone-dji:FlightPitchDegree']

                return alt, roll, yaw, pitch
