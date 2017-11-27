# RTX Reasoning Tool proof-of-concept (POC) software

## RTX team's institutional affiliations

- Oregon State University (Lead Proposing Institution)
- Institute for Systems Biology (Subaward #1)
- Ohio State University (Subaward #2)

## RTX leadership team

| Name           | Role                                        | Email                             | GitHub username                               | Areas of relevant expertise      |
| -------------- | ------------------------------------------- | --------------------------------- | --------------------------------------------- | -------------------------------- |
| Stephen Ramsey | Project PI, Oregon State University         | `stephen.ramsey@oregonstate.edu`  | [saramsey](https://github.com/saramsey)       | compbio, systems biology         |
| David Koslicki | Project Co-PI, Oregon State University      | `dkoslicki@math.oregonstate.edu`  | [dkoslicki](https://github.com/dkoslicki)     | compbio, graph algorithms        |
| Eric Deutsch   | PI, subaward, Institute for Systems Biology | `eric.deutsch@systemsbiology.org` | [edeutsch](https://github.com/edeutsch)       | bioinformatics, data management  | 
| Arnab Nandi    | PI, subaward, Ohio State University         | `arnab@cse.ohio-state.edu`        | [arnabdotorg](https://gitnub.com/arnabdotorg) | UI for querying knowledge-bases  |

## RTX other key personnel

| Name             | Affiliation                   | Email                                 | GitHub username                                     | Areas of relevant expertise |
| ---------------- | ----------------------------- | ------------------------------------- | --------------------------------------------------- | --------------------------- |
| Liang Huang      | Oregon State University       | `liang.huang@oregonstate.edu`         | [lianghuang3](https://github.com/lianghuang3)       | natural language processing | 
| Arash Termehchy  | Oregon State University       | `arash.termehchy@oregonstate.edu`     | [arashtermehchy](https://github.com/arashtermehchy) | databases, nowledge graphs  |
| Theo Knijnenburg | Institute for Systems Biology | `theo.knijnenburg@systemsbiology.org` | [tknijnen](https://github.com/tknijnen)             | systems biology, Translator |
| Sui Huang MD PhD | Institute for Systems Biology | `sui.huang@systemsbiology.org`        |                                                     | medicine, systems biology   |
| Gustavo Glusman  | Institute for Systems Biology | `gustavo.glusman@systemsbiology.org`  |                                                     | computational genomics      |

## Organization of this repository

### subdirectory `code`

All software code files for the RTX proof-of-concept are accessible (and
version-controlled) under this subdirectory. The RTX POC code is 97% Python3,
with the remainder being small bash scripts, Cypher queries, etc.

### subdirectory `data`

Text data files for the RTX system that are deployed using git are stored under
this subdirectory. There are only a few such files because the RTX POC software
obtaines most of the information that makes up the biomedical knowledge graph by
RESTfully querying web-based knowledge sources, rather than by loading flat-files.

### subdirectory `team-private`

This subdirectory contains notes other documents for sharing within the RTX team.

### License

The software that we would develop if awarded OT2 research support to build RTX
would be made publicly available, under the MIT open-source software license, in
the [RTX GitHub area](https://github.com/RTXteam/RTX).

### Dependencies outside of GitHub

- RTX depends on a (46 GB) SQLite cache file, `orangeboard.sqlite`, which is
  stored in Amazon S3 (access can be arranged upon request of the RTX project
  leadership team).

- Neo4j and Python modules: see [the README the code subdirectory](https://github.com/dkoslicki/NCATS/blob/master/code/README.md)


### Issue tracking

Our team makes extensive use of the GitHub Issues system for project
management. Browsing the open and closed
[RTX issues](https://github.com/dkoslicki/NCATS/issues) will provide a sense of
our team's workflow and organizational style, at least for a one-month POC
project.

 

