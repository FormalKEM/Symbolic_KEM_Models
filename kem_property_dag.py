from dagpruner import DAGPruner

kem_property_map = {
    1: "bindcttopk",  # CT-PK
    2: "bindkcttopk",  # K,CT-PK
    3: "bindcttok",  # CT-K
    4: "bindktopk",  # K-PK
    5: "bindktoct",  # K-CT
    6: "bindpkktoct",  # PK,K-CT
}


def encode_property_and_add_to_dag(dag, iterable) -> str:
    # Returns the prop name
    prop_name = get_property_name(iterable)
    dag.add_node(prop_name)
    return prop_name


def get_property_name(iterable):
    return ", ".join(str(kem_property_map[x]) for x in iterable)


def get_kem_property_dag(name: str):
    dag = DAGPruner(name)
    # ============================================================
    # Define node names
    node1 = encode_property_and_add_to_dag(dag, [5, 1])
    node2 = encode_property_and_add_to_dag(dag, [6, 4, 1])
    node3 = encode_property_and_add_to_dag(dag, [5, 4, 3])

    node4 = encode_property_and_add_to_dag(dag, [4, 1])
    node5 = encode_property_and_add_to_dag(dag, [6, 1])
    node6 = encode_property_and_add_to_dag(dag, [6, 4, 3])
    node7 = encode_property_and_add_to_dag(dag, [5, 4])
    node8 = encode_property_and_add_to_dag(dag, [5, 2, 3])
    node9 = encode_property_and_add_to_dag(dag, [1])
    node10 = encode_property_and_add_to_dag(dag, [4, 3])
    node11 = encode_property_and_add_to_dag(dag, [6, 2, 3])
    node12 = encode_property_and_add_to_dag(dag, [6, 4])
    node13 = encode_property_and_add_to_dag(dag, [5, 2])
    node14 = encode_property_and_add_to_dag(dag, [5, 3])
    node15 = encode_property_and_add_to_dag(dag, [2, 3])
    node16 = encode_property_and_add_to_dag(dag, [6, 5, 1])
    node17 = encode_property_and_add_to_dag(dag, [6, 3])
    node18 = encode_property_and_add_to_dag(dag, [5])
    node19 = encode_property_and_add_to_dag(dag, [2])
    node20 = encode_property_and_add_to_dag(dag, [3])
    node21 = encode_property_and_add_to_dag(dag, [4])
    node22 = encode_property_and_add_to_dag(dag, [6])
    # =============================================================
    # Add edges
    dag.add_edge(node1, node2)
    dag.add_edge(node1, node3)

    dag.add_edge(node2, node4)
    dag.add_edge(node2, node5)
    dag.add_edge(node2, node6)

    dag.add_edge(node3, node6)
    dag.add_edge(node3, node7)
    dag.add_edge(node3, node8)

    dag.add_edge(node4, node9)
    dag.add_edge(node4, node10)

    dag.add_edge(node5, node9)
    dag.add_edge(node5, node11)

    dag.add_edge(node6, node10)
    dag.add_edge(node6, node11)
    dag.add_edge(node6, node12)

    dag.add_edge(node7, node12)
    dag.add_edge(node7, node13)

    dag.add_edge(node8, node14)
    dag.add_edge(node8, node13)
    dag.add_edge(node8, node11)

    dag.add_edge(node9, node19)
    dag.add_edge(node9, node20)

    dag.add_edge(node10, node15)
    dag.add_edge(node10, node21)

    dag.add_edge(node11, node15)
    dag.add_edge(node11, node16)
    dag.add_edge(node11, node17)

    dag.add_edge(node12, node16)
    dag.add_edge(node12, node21)

    dag.add_edge(node13, node16)
    dag.add_edge(node13, node18)

    dag.add_edge(node14, node18)
    dag.add_edge(node14, node20)

    dag.add_edge(node15, node19)
    dag.add_edge(node15, node20)

    dag.add_edge(node16, node19)
    dag.add_edge(node16, node22)

    dag.add_edge(node17, node20)
    dag.add_edge(node17, node22)

    dag.add_edge(node18, node22)

    dag.add_edge(node21, node19)

    return dag


def get_mal_kem_property_dag(name: str):
    dag = DAGPruner(name)

    node1 = encode_property_and_add_to_dag(dag, [5, 1, 3])
    node2 = encode_property_and_add_to_dag(dag, [5, 1])
    node3 = encode_property_and_add_to_dag(dag, [5, 4, 3])
    node4 = encode_property_and_add_to_dag(dag, [6, 4, 1, 3])
    node5 = encode_property_and_add_to_dag(dag, [6, 4, 1])
    node6 = encode_property_and_add_to_dag(dag, [5, 4])
    node7 = encode_property_and_add_to_dag(dag, [6, 4, 3])
    node8 = encode_property_and_add_to_dag(dag, [5, 2, 3])
    node9 = encode_property_and_add_to_dag(dag, [4, 1, 3])
    node10 = encode_property_and_add_to_dag(dag, [6, 1, 3])
    node11 = encode_property_and_add_to_dag(dag, [4, 1])
    node12 = encode_property_and_add_to_dag(dag, [6, 1])
    node13 = encode_property_and_add_to_dag(dag, [6, 4])
    node14 = encode_property_and_add_to_dag(dag, [5, 2])
    node15 = encode_property_and_add_to_dag(dag, [4, 3])
    node16 = encode_property_and_add_to_dag(dag, [6, 2, 3])
    node17 = encode_property_and_add_to_dag(dag, [5, 3])
    node18 = encode_property_and_add_to_dag(dag, [1, 3])
    node19 = encode_property_and_add_to_dag(dag, [4])
    node20 = encode_property_and_add_to_dag(dag, [1])
    node21 = encode_property_and_add_to_dag(dag, [2])
    node22 = encode_property_and_add_to_dag(dag, [6, 2])
    node23 = encode_property_and_add_to_dag(dag, [6])
    node24 = encode_property_and_add_to_dag(dag, [5])
    node25 = encode_property_and_add_to_dag(dag, [2, 3])
    node26 = encode_property_and_add_to_dag(dag, [6, 3])
    node27 = encode_property_and_add_to_dag(dag, [3])

    dag.add_edge(node1, node2)
    dag.add_edge(node1, node3)
    dag.add_edge(node1, node4)

    dag.add_edge(node2, node5)
    dag.add_edge(node2, node6)

    dag.add_edge(node3, node6)
    dag.add_edge(node3, node7)
    dag.add_edge(node3, node8)

    dag.add_edge(node4, node5)
    dag.add_edge(node4, node7)
    dag.add_edge(node4, node9)
    dag.add_edge(node4, node10)

    dag.add_edge(node5, node11)
    dag.add_edge(node5, node12)
    dag.add_edge(node5, node13)

    dag.add_edge(node6, node13)
    dag.add_edge(node6, node14)

    dag.add_edge(node7, node13)
    dag.add_edge(node7, node15)
    dag.add_edge(node7, node16)

    dag.add_edge(node8, node14)
    dag.add_edge(node8, node16)
    dag.add_edge(node8, node17)

    dag.add_edge(node9, node15)
    dag.add_edge(node9, node18)
    dag.add_edge(node9, node11)

    dag.add_edge(node10, node18)
    dag.add_edge(node10, node16)
    dag.add_edge(node10, node12)

    dag.add_edge(node11, node19)
    dag.add_edge(node11, node20)

    dag.add_edge(node12, node20)
    dag.add_edge(node12, node22)

    dag.add_edge(node13, node19)
    dag.add_edge(node13, node22)

    dag.add_edge(node14, node24)
    dag.add_edge(node14, node21)

    dag.add_edge(node15, node19)
    dag.add_edge(node15, node25)

    dag.add_edge(node16, node25)
    dag.add_edge(node16, node26)

    dag.add_edge(node17, node26)
    dag.add_edge(node17, node24)

    dag.add_edge(node18, node20)
    dag.add_edge(node18, node25)

    dag.add_edge(node19, node21)

    dag.add_edge(node20, node21)

    dag.add_edge(node22, node21)
    dag.add_edge(node22, node23)

    dag.add_edge(node24, node23)

    dag.add_edge(node25, node27)
    dag.add_edge(node25, node21)

    dag.add_edge(node26, node23)
    dag.add_edge(node26, node27)

    return dag


if __name__ == "__main__":
    dag = get_kem_property_dag("Test2")
    dag.report_proof("bindktoct, bindcttok")
    dag.report_counterexample("bindktopk, bindcttok")
    dag.report_timeout("bindktoct, bindktopk")
    dag.render_dot()

    mal_dag = get_mal_kem_property_dag("Test_Mal")
    mal_dag.render_dot()
