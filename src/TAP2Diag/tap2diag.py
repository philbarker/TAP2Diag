from tap2shacl import TAP2APConverter

class TAP2DiagConverter:
    """Read in a TAP as pyhton AP then convert to Mermaid code."""

    def __init__(self, tap_fname, config_fname, ns_fname, shapes_fname, about_fname):
        converter = TAP2APConverter(tap_fname, config_fname)
        converter.ap.load_namespaces(ns_fname)
        converter.ap.load_shapeInfo(shapes_fname)
        converter.convert_TAP_AP()
        converter.load_AP_Metadata(about_fname)
        self.ap=converter.ap
        self.mermaid=list()

    def convertAP2mermaid(self):
        self._appendMetadata()
        self.mermaid.append("classDiagram")
        self._appendClasses()
        self._appendProperties()
        return self.mermaid
    
    def _appendMetadata(self):
        metadata = self.ap.metadata
        mermaid = self.mermaid
        mermaid.append("---")
        for key in metadata.keys():
            mermaid.append(f"{key}: {metadata[key]}")
        mermaid.append("---")
        return mermaid

    def _appendClasses(self):
        mermaid = self.mermaid
        shapeDict=self.ap.shapeInfo
        for shape in shapeDict.values():
            if self._used_by_templates(shape):
                mermaid.append(f"\tclass {shape.id}")
                self._addTargets(shape.targets, shape)
        return mermaid


    def dump_mermaid(self, fname = None):
        """Print the mermaid code to a file or the terminal."""
        if fname :
            if fname.split(".")[-1] == "md": 
                markdown = True
            try:
                f = open(fname, "w")
            except Exception as e:
                print(f"Could not open file {fname} for writing.")
                raise e
            print(f"Writing mermaid file to {fname}")
            if markdown:
                f.write("Mermaid diagram created by TAP2Diag\n")
                f.write("\n```mermaid\n")
            for line in self.mermaid:
                f.write(f"{line}\n")
            if markdown:
                f.write("```\n")
            f.close()

        else:
            for line in self.mermaid:
                print(line)

    def _appendProperties(self):
        mermaid = self.mermaid
        for t in self.ap.statementTemplates:
            l = ""
            for lang in t.labels.keys():
                l = f"{l}{t.labels[lang]}"
            if t.valueShapes: # it's an object property
                for d in t.shapes:
                    for r in t.valueShapes:
                        for p in t.properties:
                            d = decolonize(d)
                            r = decolonize(r)
                            p = decolonize(p)
                            mermaid.append(f"\t{d} --> {r} : {p} #40;{l}#41;")
            else:                       # it's a data property
                for d in t.shapes:
                    for p in t.properties:
                        d = decolonize(d)
                        p = decolonize(p)
                        mermaid.append(f"\t{d} : {p} #40;{l}#41;")

    def _used_by_templates(self, shapeInfo):
        """Return True iff the shapeID is used by any statement templates."""
        id = shapeInfo.id
        for t in self.ap.statementTemplates:
            if id in t.shapes:
                return True
            if id in t.valueShapes:
                return True
        return False

    def _addTargets(self, targets, shape):
        mermaid = self.mermaid
        if targets is not {}:
            for key in targets.keys():
                for target in targets[key]:
                    target = decolonize(target)
                    t = f"{key} {target}"
                    mermaid.append(f"\t{shape.id} : target({t})")



def decolonize(s):
    return "#58;".join(s.split(":"))






        

