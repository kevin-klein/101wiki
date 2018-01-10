import sys
sys.path.append('/Users/kevinklein/javalang')

from worker.models import *

e = JavaExtractor()
fragments = e.extract("""
package org.softlang.company.features;

import org.softlang.company.xjc.*;

public class Total {

    public static double total(Company c) {
        double total = 0;
        for (Department d : c.getDepartment())
            total += total(d);
        return total;
    }

    public static double total(Department d) {
        double total = total(d.getManager());
        for (Subunit s : d.getSubunit())
            total += total(s);
        return total;
    }

    public static double total(Employee e) {
        return e.getSalary();
    }

    //
    // We cannot use virtual methods.
    // That is, we do not allow ourselves modifying schema-derived classes.
    //
    public static double total(Subunit s) {
        if (s instanceof Department)
            return total(((Department)s));
        else if (s instanceof Employee)
            return total(((Employee)s));
        else throw new IllegalArgumentException();
    }

}

""")

import json

# print(json.dumps(fragments, indent=4))

e2 = JavaScriptExtractor()
fragments = e2.extract("""
var x = function(y) {
	return 5;
}

function extractFloat(o){return parseFloat(o.textContent);}
function setFloat(o,v){o.textContent = v;}
function allTrue(arr){
  var ret = true;
  jQuery.each(arr,function(i,a){ret = ret && a;});
  return ret;
}
function cut(){
  $(".salary > .int").contents().each(function(){
    var old = extractFloat(this);
    setFloat(this, old/2);
  });
}
function total(){
  var t = 0;
  $(".salary > .int").contents().each(function(){
    t = t + extractFloat(this);
  });
  alert(t);
}
// todo: works now but I think it is doing extra calculation by finding the departments more than once.
function depth(jqo){
  var depts = $(jqo).find(".department")
  var depths = jQuery.map(depts,function(a){return depth($(a));});
  var add = 0;
  if (jqo.attr("class") == "department"){add = 1;}
  if (depths.length == 0) {return add;} else {return  (Math.max.apply(null, depths) + add);}
}
function check_precedence(m,jqo){
  if (jqo.attr("class") ==  "department") {
    var manager_sal = parseFloat(jqo.children().slice(1,2).children().slice(2,3).first().text())
    return allTrue(jqo.children().slice(2).map(function(){return check_precedence(manager_sal, $(this))}));
  }
  else if (jqo.attr("class") ==  "employee") {
    var employee_sal = parseFloat(jqo.children().slice(2,3).first().text());
    return (m > employee_sal);
  }
  else if (jqo.attr("class") ==  "manager") {
    var manager_sal = parseFloat(jqo.children().slice(2,3).first().text());
    return (m > manager_sal);
  }
  else {
    return allTrue(jqo.children().map(function(){return check_precedence(m, $(this))}));
  }
}
""")

# print(json.dumps(fragments, indent=4))


e3 = PythonExtractor()
fragments = e3.extract("""
from .worker import *

import javalang
import javalang.tree

import esprima

import ast

class JavaExtractor(object):
    i = 12345

    def extract(self, source):
        self.source = source
        tree = javalang.parse.parse(source)

        return {
        'imports': self._extract_imports(tree),
        'package': self._extract_package(tree),
        'fragments': self._extract_fragments(tree)
        }

    def _extract_annotations(self, tree):
        return [annotation.name for annotation in tree.annotations]

""")

print(fragments)

with open('worker/models.py') as f:
    print(json.dumps(e3.extract(f.read()), indent=4))
