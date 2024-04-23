from kfp import dsl
from kfp.dsl import Artifact, Input, Output


@dsl.container_component
def merge_jsons(
    one_json_file: Input[Artifact],
    another_json_file: Input[Artifact],
    merged_json_file: Output[Artifact],
):
    merged_json_file.uri = dsl.ConcatPlaceholder([merged_json_file.uri, ".tar"])
    return dsl.ContainerSpec(
        image="ddev/ddev-utilities",
        command=[
            "sh",
            "-xc",
            "sleep 5 && mkdir -p $(dirname $2) && jq -c '.[]' $1 >> $2 && jq -c '.[]' $3 >> $2",
        ],
        args=[
            one_json_file.path,
            another_json_file.path,
            merged_json_file.path,
        ],
    )


@dsl.pipeline()
def merge_two_json_files(
    one_json_file: str,
    another_json_file: str,
):
    one_json_importer_task = dsl.importer(
        artifact_uri=one_json_file,
        artifact_class=Artifact,
        reimport=False,
    )
    another_json_importer_task = dsl.importer(
        artifact_uri=another_json_file,
        artifact_class=Artifact,
        reimport=False,
    )

    example_task = merge_jsons(
        one_json_file=one_json_importer_task.output,
        another_json_file=another_json_importer_task.output,
    )


if __name__ == "__main__":
    import kfp.compiler as compiler

    compiler.Compiler().compile(merge_two_json_files, "pipeline.yaml")
