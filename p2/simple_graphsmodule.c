#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"

typedef struct {
    PyObject_HEAD
    unsigned short vertices;
    short* edges;
} GraphObject;

static void
Graph_dealloc(GraphObject* self)
{
    Py_XDECREF(self->edges);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject*
Graph_new(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    GraphObject* self;
    self = (GraphObject*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->vertices = 0;
        self->edges = (short*)malloc(sizeof(short) * 16);
        for (int i = 0; i < 16; i++) {
            self->edges[i] = 0;
        }
        if (self->edges == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject*)self;
}

static short
vertices_from_text(char* text) {
    short size = (int)text[0] - 63;
    return (unsigned short)~(65535 << size);
}

static short
edges_from_text(char* text, short* edges) {
    int size = (int)text[0] - 63;
    int k = 0;
    int i = 1;
    int c = 0;
    for (int v = 1; v < size; v++) {
        for (int u = 0; u < v; u++) {
            if (k == 0) {
                c = (int)text[i] - 63;
                i++;
                k = 6;
            }
            k--;
            if ((c & (1 << k)) != 0) {
                edges[u] = edges[u] | 1 << v;
                edges[v] = edges[v] | 1 << u;
            }
        }
    }
}

static int
Graph_init(GraphObject* self, PyObject* args, PyObject* kwds)
{
    static char* kwlist[] = { "text", NULL };
    char* text = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s", kwlist, &text)) {
        return -1;
    }

    if (text) {
        self->vertices = vertices_from_text(text);
        edges_from_text(text, self->edges);
    }
    return 0;
}

static PyObject*
Graph_number_of_vertices(GraphObject* self, PyObject* Py_UNUSED(ignored))
{
    if (self->vertices == NULL) {
        PyErr_SetString(PyExc_AttributeError, "vertices");
        return NULL;
    }
    int result = 0;
    for (int i = 0; i < 16; i++) {
        if (self->vertices & (1 << i)) result++;
    }

    return Py_BuildValue("i", result);
}

static PyObject*
Graph_vertices(GraphObject* self, PyObject* Py_UNUSED(ignored))
{
    PyObject* set = PySet_New(NULL);
    for (int i = 0; i < 16; i++) {
        if (self->vertices & 1<<i) {
            PyObject* ver_int = Py_BuildValue("i", i);
            PySet_Add(set, ver_int);
        }
    }

    return set;
}

static PyObject*
Graph_edges(GraphObject* self, PyObject* Py_UNUSED(ignored))
{
    if (self->edges == NULL) {
        PyErr_SetString(PyExc_AttributeError, "edges");
        return NULL;
    }
    PyObject* result = PySet_New(NULL);
    for (int v = 0; v < 16; v++) {
        short edges_short = self->edges[v];
        for (int u = v; u < 16; u++) {
            if (edges_short & 1 << u) {
                PyObject* e1 = Py_BuildValue("i", v);
                PyObject* e2 = Py_BuildValue("i", u);
                PyObject* edges = PyTuple_Pack(2, e1, e2);
                PySet_Add(result, edges);
                Py_DECREF(edges);
            }
        }
    }

    return result;
}

static PyObject*
Graph_vertex_degree(GraphObject* self, PyObject* args)
{
    int v = NULL;
    if (!PyArg_ParseTuple(args, "i", &v)) {
        return -1;
    }

    int result = 0;
    for (int i = 0; i < 16; i++) {
        if (self->edges[v] & (1 << i)) result++;
    }

    return Py_BuildValue("i", result);
}

static PyObject*
Graph_vertex_neighbors(GraphObject* self, PyObject* args)
{
    int v = NULL;
    PyObject *result;
    if (!PyArg_ParseTuple(args, "i", &v)) {
        return -1;
    }

    result = PySet_New(NULL);
    short edges_short = self->edges[v];
    for (int i = 0; i < 16; i++) {
        if (edges_short & 1 << i) {
            PyObject* neighbor = Py_BuildValue("i", i);
            PySet_Add(result, neighbor);
        }
    }

    return result;
}

static PyObject*
Graph_add_vertex(GraphObject* self, PyObject* args)
{
    int v = NULL;
    if (!PyArg_ParseTuple(args, "i", &v)) {
        return -1;
    }

    self->vertices = self->vertices | 1 << v;
    Py_RETURN_NONE;
}

static PyObject*
Graph_delete_vertex(GraphObject* self, PyObject* args)
{
    int v = NULL;
    if (!PyArg_ParseTuple(args, "i", &v)) {
        return -1;
    }

    unsigned short mask = (0xFFFE << v | 0x7FFF >> (15 - v));
    self->vertices = self->vertices & mask;
    self->edges[v] = 0;
    for (int i = 0; i < 16; i++) {
        self->edges[i] = self->edges[i] & mask;
    }
    Py_RETURN_NONE;
}

static PyObject*
Graph_is_edge(GraphObject* self, PyObject* args)
{
    int v1 = NULL, v2 = NULL;
    if (!PyArg_ParseTuple(args, "ii", &v1, &v2)) {
        return -1;
    }
    if (self->edges[v1] & 1 << v2) {
        Py_RETURN_TRUE;
    }
    else{
        Py_RETURN_FALSE;
    }
}

static PyObject*
Graph_add_edge(GraphObject* self, PyObject* args)
{
    int v1 = NULL, v2 = NULL;
    if (!PyArg_ParseTuple(args, "ii", &v1, &v2)) {
        return -1;
    }
    self->edges[v1] = self->edges[v1] | 1 << v2;
    self->edges[v2] = self->edges[v2] | 1 << v1;
    Py_RETURN_NONE;
}

static PyObject*
Graph_delete_edge(GraphObject* self, PyObject* args)
{
    int v1 = NULL, v2 = NULL;
    if (!PyArg_ParseTuple(args, "ii", &v1, &v2)) {
        return -1;
    }
    self->edges[v1] = self->edges[v1] & (0xFFFE << v2 | 0x7FFF >> (15 - v2));
    self->edges[v2] = self->edges[v2] & (0xFFFE << v1 | 0x7FFF >> (15 - v1));
    Py_RETURN_NONE;
}

static PyObject*
Graph_number_of_edges(GraphObject* self, PyObject* args)
{
    int result = 0;
    for (int i = 0; i < 16; i++) {
        for (int j = i + 1; j < 16; j++) {
            if (self->edges[i] & 1 << j) {
                result++;
            }
        }
    }
    return Py_BuildValue("i", result);
}

static PyObject*
Graph_degree_sequence(GraphObject* self, PyObject* args)
{
    int v_num = 0, result;
    for (int i = 0; i < 16; i++) {
        if (self->vertices & (1 << i)) v_num++;
    }
    PyObject* list = PyList_New(v_num);
    int k = 0;
    for (int i = 0; i < 16; i++) {
        if (self->vertices & (1 << i)) {
            result = 0;
            for (int j = 0; j < 16; j++) {
                if (self->edges[i] & 1 << j) {
                    result++;
                }
            }
            PyObject* deg = Py_BuildValue("i", result);
            PyList_SetItem(list, k, deg);
            k++;
        }
    }
    PyList_Sort(list);
    PyList_Reverse(list);
    return list;
}

static PyMethodDef Graph_methods[] = {
    {"vertices", (PyCFunction)Graph_vertices, METH_NOARGS},
    {"number_of_vertices", (PyCFunction)Graph_number_of_vertices, METH_NOARGS},
    {"vertex_degree", (PyCFunction)Graph_vertex_degree, METH_VARARGS},
    {"vertex_neighbors", (PyCFunction)Graph_vertex_neighbors, METH_VARARGS},
    {"edges", (PyCFunction)Graph_edges, METH_NOARGS},
    {"add_vertex", (PyCFunction)Graph_add_vertex, METH_VARARGS},
    {"delete_vertex", (PyCFunction)Graph_delete_vertex, METH_VARARGS},
    {"is_edge", (PyCFunction)Graph_is_edge, METH_VARARGS},
    {"add_edge", (PyCFunction)Graph_add_edge, METH_VARARGS},
    {"delete_edge", (PyCFunction)Graph_delete_edge, METH_VARARGS},
    {"number_of_edges", (PyCFunction)Graph_number_of_edges, METH_NOARGS},
    {"degree_sequence", (PyCFunction)Graph_degree_sequence, METH_NOARGS},
    {NULL}  /* Sentinel */
};

static PyTypeObject CustomType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "simple_graphs.AdjacencyMatrix",
    .tp_doc = "Graph it is",
    .tp_basicsize = sizeof(GraphObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = Graph_new,
    .tp_init = (initproc)Graph_init,
    .tp_dealloc = (destructor)Graph_dealloc,
    .tp_methods = Graph_methods,
};

static PyModuleDef custommodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "simple_graphs",
    .m_doc = "Graph module",
    .m_size = -1,
};

PyMODINIT_FUNC
PyInit_simple_graphs(void)
{
    PyObject* m;
    if (PyType_Ready(&CustomType) < 0)
        return NULL;

    m = PyModule_Create(&custommodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&CustomType);
    if (PyModule_AddObject(m, "AdjacencyMatrix", (PyObject*)&CustomType) < 0) {
        Py_DECREF(&CustomType);
        Py_DECREF(m);
        return NULL;
    }

    return m;
}

int main() {
    return 0;
}