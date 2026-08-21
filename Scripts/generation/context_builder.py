def build_context(results):

    """
    Construit le contexte scientifique pour le LLM.

    Les chunks appartenant au même article
    sont regroupés sous un même article.
    """

    if not results:

        return "No scientific context was retrieved."


    articles = {}


    for result in results:

        payload = result.payload or {}

        pmcid = payload.get(
            "pmcid",
            "Unknown"
        )

        if pmcid not in articles:

            articles[pmcid] = {
                "pmcid": pmcid,
                "chunks": []
            }


        articles[pmcid]["chunks"].append({

            "chunk_id": payload.get(
                "chunk_id",
                "Unknown"
            ),

            "path": payload.get(
                "path",
                "Unknown"
            ),

            "text": payload.get(
                "text",
                ""
            ),

            "score": result.score
        })


    context_parts = []


    for article in articles.values():

        source_parts = []

        source_parts.append(
            f"ARTICLE: {article['pmcid']}"
        )

        source_parts.append(
            "This context comes from one scientific article."
        )

        source_parts.append("")


        for chunk_index, chunk in enumerate(
            article["chunks"],
            start=1
        ):

            source_parts.append(
                f"CHUNK {chunk_index}"
            )

            source_parts.append(
                f"SECTION: {chunk['path']}"
            )

            source_parts.append(
                f"CHUNK ID: {chunk['chunk_id']}"
            )

            source_parts.append(
                "TEXT:"
            )

            source_parts.append(
                chunk["text"]
            )

            source_parts.append("")


        context_parts.append(
            "\n".join(
                source_parts
            ).strip()
        )


    return "\n\n".join(
        context_parts
    )