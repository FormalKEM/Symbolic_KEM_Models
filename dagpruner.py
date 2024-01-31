from __future__ import annotations

import graphviz


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children = list()
        self.parents = list()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_child(self, child: Node) -> None:
        self.children.append(child)

    def add_parent(self, parent: Node) -> None:
        self.parents.append(parent)


class DAGPruner:
    def __init__(self, lemma_name: str) -> None:
        self.lemma_name = lemma_name
        # Dict of node.name -> Node
        # The following invariant should hold:
        # nodes.values() == open_nodes \/ proven_nodes \/ cex_nodes \/ timeout_nodes
        self.nodes = dict()
        # Set of open nodes
        self.open_nodes = set()
        # Set of proven nodes
        self.proven_nodes = set()
        # Set of counterexample nodes
        self.cex_nodes = set()
        # Set of timed out nodes
        self.timeout_nodes = set()

    def add_node(self, node_name: str) -> None:
        node = Node(node_name)
        self.nodes[node.name] = node
        self.open_nodes.add(node)

    def add_edge(self, source_name: str, target_name: str) -> None:
        assert source_name in self.nodes.keys()
        assert target_name in self.nodes.keys()
        self._add_edge(self.nodes[source_name], self.nodes[target_name])

    def _add_edge(self, source: Node, target: Node) -> None:
        assert source.name in self.nodes.keys()
        assert target.name in self.nodes.keys()
        source.add_child(target)
        target.add_parent(source)

    def report_timeout(self, node_name: str) -> None:
        assert node_name in self.nodes.keys()
        assert self.nodes[node_name] in self.open_nodes

        node = self.nodes[node_name]
        self.open_nodes.remove(node)
        self.timeout_nodes.add(node)

    def report_proof(self, node_name: str) -> None:
        assert node_name in self.nodes.keys()
        self._propagate_proof_result(self.nodes[node_name])

    def _propagate_proof_result(self, node: Node) -> None:
        if node in self.open_nodes:
            self.open_nodes.remove(node)
        elif node in self.proven_nodes:
            pass
        elif node in self.timeout_nodes:
            self.timeout_nodes.remove(node)
        else:
            self.cex_nodes.remove(node)

        self.proven_nodes.add(node)
        for parent in node.parents:
            # Terminates since we are dealing with a DAG
            self._propagate_proof_result(parent)

    def report_counterexample(self, node_name: str) -> None:
        assert node_name in self.nodes.keys()
        self._propagate_counterexample_result(self.nodes[node_name])

    def _propagate_counterexample_result(self, node: Node) -> None:
        if node in self.open_nodes:
            self.open_nodes.remove(node)
        elif node in self.cex_nodes:
            pass
        elif node in self.timeout_nodes:
            self.timeout_nodes.remove(node)
        else:
            self.proven_nodes.remove(node)

        self.cex_nodes.add(node)
        for child in node.children:
            # Terminates since we are dealing with a DAG
            self._propagate_counterexample_result(child)

    def get_next_property(self) -> str:
        next_prop = self.open_nodes.pop()
        self.open_nodes.add(next_prop)
        return next_prop.name

    def render_dot(self) -> None:
        dot = graphviz.Digraph(comment=self.lemma_name)
        # Add all nodes
        for node in self.nodes.values():
            dot.attr("node", style="filled", color=self.get_node_color(node))
            dot.node(node.name, node.name)

        # Add all edges
        for node in self.nodes.values():
            for child in node.children:
                dot.edge(node.name, child.name)

        dot.render(self.lemma_name + "_dag.gv")

    def get_node_color(self, node: Node) -> str:
        if node in self.timeout_nodes:
            return "yellow"
        elif node in self.proven_nodes:
            return "green"
        elif node in self.cex_nodes:
            return "red"
        else:
            return ""

    def is_fully_explored(self):
        return len(self.open_nodes) == 0

    def get_solution_set(self) -> set(str):
        return {
            node.name
            for node in filter(self._is_node_solution_node, self.nodes.values())
        }

    def _is_node_solution_node(self, node: Node) -> bool:
        if node not in self.proven_nodes:
            return False

        return all(
            map(lambda x: x in self.timeout_nodes or x in self.cex_nodes, node.children)
        )


if __name__ == "__main__":
    pass
