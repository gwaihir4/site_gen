
class HTMLNode():
    def __init__(self, tag = None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html_str = ""
        if self.props is None:
            return 
        for tag, value in self.props.items():
            # for tag, value in pair:
                    html_str += f' {tag}="{value}"'
        return html_str # str -> html version href="www.google.com"
    
    def __repr__(self):
        return (f"HTMLNode ({self.tag}, {self.value}, {self.children}, {self.props})")
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None): # can add None for children
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        html_str = ""
        if self.value == None:
             raise ValueError()
        if self.tag == None:
            return f"{self.value}"
        if self.props != None:
            html_str += f"<{self.tag}"
            html_str += self.props_to_html()
            html_str += f">{self.value}</{self.tag}>"
            return html_str
        html_str += f'<{self.tag}>{self.value}</{self.tag}>'
        return html_str

class ParentNode (HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError()
        if self.children == None:
            raise ValueError()
        else:
            html_str = ""
            html_str += f"<{self.tag}>"
            if self.props != None:  
                for prop in self.props:
                    html_str += self.props_to_html()
            for child in self.children:
                html_str += child.to_html()
        html_str += f"</{self.tag}>"
        return html_str
