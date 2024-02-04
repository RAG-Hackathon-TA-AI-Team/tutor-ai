import base64
from typing import Sequence, Any, List

from app.engine.schema import VideoMetaType
from app.engine.schema import create_transcript_doc, create_keyframe_doc
from llama_index.node_parser.interface import NodeParser
from llama_index.node_parser import SentenceSplitter
from llama_index.schema import BaseNode, Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

SYSTEM_MESSAGE = """\
You are an expert in describing a sequence of continuous frames in a video. Given
several frames, provide a alternative text corresponding to the content, action, phenomenon, or
event in the video. The text should be detailed and descriptive, and should be able to convey the
content of the video to a person who is unable to see it. 1 paragraph maximum.
"""


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_frames_to_text_chain():
    vision_llm = ChatOpenAI(
        model_name="gpt-4-vision-preview",
        max_tokens=4096,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=SYSTEM_MESSAGE),
            MessagesPlaceholder(variable_name="frames")
        ]
    )

    return prompt | vision_llm | StrOutputParser()


def parse_transcript_nodes(docs: List[Document]) -> List[BaseNode]:
    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=32)
    nodes = splitter.get_nodes_from_documents(docs)
    return [
        create_transcript_doc(
            node.metadata["video_path"],
            node.metadata["start_time"],
            node.metadata["end_time"],
            node.text,
        )
        for node in nodes
    ]


def parse_keyframe_nodes(docs: List[Document]) -> List[BaseNode]:
    frames_to_text_chain = get_frames_to_text_chain()

    chain_inputs = []
    for doc in docs:
        frames = doc.metadata['frames']
        encoded_images = [
            encode_image(frame_path)
            for frame_path in frames
        ]
        human_message = HumanMessage(content=[
            {"type": "text", "text": "Provide a detailed description of the following frames:"},
            *[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                        "detail": "auto",
                    },
                }
                for encoded_image in encoded_images
            ]
        ])
        chain_inputs.append({
            "frames": human_message,
        })

    # parallelize the model invocations
    descriptions = frames_to_text_chain.batch(chain_inputs)

    results = []
    for i, doc in enumerate(docs):
        results.append(
            create_keyframe_doc(
                doc.metadata["video_path"],
                doc.metadata["start_time"],
                doc.metadata["end_time"],
                doc.metadata["frames"],
                descriptions[i],
            )
        )

    return results


class VideoNodeParser(NodeParser):
    include_metadata: bool = False
    include_prev_next_rel: bool = False

    def _parse_nodes(
            self,
            nodes: Sequence[Document],
            show_progress: bool = False,
            **kwargs: Any,
    ) -> List[BaseNode]:
        transcript_nodes = [node for node in nodes if node.metadata["type"] == VideoMetaType.TRANSCRIPT]
        keyframe_nodes = [node for node in nodes if node.metadata["type"] == VideoMetaType.KEYFRAME]

        return parse_transcript_nodes(transcript_nodes) + parse_keyframe_nodes(keyframe_nodes)
