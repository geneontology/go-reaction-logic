"""Main python file."""
from dataclasses import dataclass
from typing import List

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A
from oaklib.interfaces import OboGraphInterface, MappingProviderInterface
from oaklib.types import CURIE
from pydantic import BaseModel

HAS_PARTICIPANT = "RO:0000057"


class ChemicalEntity(BaseModel):
    """A chemical entity."""
    id: CURIE
    label: str

@dataclass
class GOReactionEngine:

    @property
    def go_adapter(self) -> OboGraphInterface:
        return get_adapter("sqlite:obo:go")

    @property
    def rhea_adapter(self) -> OboGraphInterface:
        return get_adapter("sqlite:obo:rhea")

    @property
    def chebi_adapter(self) -> OboGraphInterface:
        return get_adapter("sqlite:obo:chebi")

    def mfs_to_rheas(self, mfs: List[CURIE]) -> List[CURIE]:
        """
        Convert a list of molecular functions to RHEA IDs.

        Example:

            >>> engine = GOReactionEngine()
            >>> rhea_ids = engine.mfs_to_rheas(["GO:0033699"])
            >>> sorted(rhea_ids)
            ['RHEA:52128', 'RHEA:52132']

            >>> engine.mfs_to_rheas(["GO:0008446"])
            ['RHEA:23820']

        :param mfs:
        :return:
        """
        go_adapter = self.go_adapter
        expanded_mfs = go_adapter.descendants(mfs, predicates=[IS_A], reflexive=True)
        if not isinstance(go_adapter, MappingProviderInterface):
            raise ValueError("Rhea adapter does not support mapping.")
        rhea_ids = set()
        for m in go_adapter.sssom_mappings(expanded_mfs, source="RHEA"):
            rhea_ids.add(m.object_id)
        return list(rhea_ids)

    def rhea_participants(self, rhea_ids: List[CURIE]) -> List[CURIE]:
        """
        Get the participants in a reaction.

        Example:

            >>> engine = GOReactionEngine()
            >>> rhea_ids = ["RHEA:23820"]
            >>> participants = engine.rhea_participants(rhea_ids)
            >>> sorted(participants)
            ['CHEBI:15377', 'CHEBI:57527', 'CHEBI:57964']

        :param rhea_ids:
        :return:
        """
        rhea_adapter = self.rhea_adapter
        participants = [o for _s, _p, o in rhea_adapter.relationships(rhea_ids, predicates=[HAS_PARTICIPANT])]
        return participants

    def mfs_to_chemicals(self, mfs: List[CURIE]) -> List[CURIE]:
        """
        Convert a list of molecular functions to chemical entities.

        Example:

            >>> engine = GOReactionEngine()
            >>> chemicals = engine.mfs_to_chemicals(["GO:0008446"])
            >>> sorted(chemicals)
            ['CHEBI:15377', 'CHEBI:57527', 'CHEBI:57964']

        :param mfs:
        :return:
        """
        reactions = self.mfs_to_rheas(mfs)
        rhea_adapter = self.rhea_adapter
        chemicals = [o for _s, _p, o in rhea_adapter.relationships(reactions, predicates=[HAS_PARTICIPANT])]
        return chemicals


    def _chebi_ids_to_entities(self, ids: List[CURIE]) -> List[ChemicalEntity]:
        chebi_adapter = self.chebi_adapter
        entities = [ChemicalEntity(id=chebi_id, label=chebi_adapter.label(chebi_id)) for chebi_id in ids]
        return entities


    def compute_intermediates(self, upstream_mf: CURIE, downstream_mf: CURIE) -> List[ChemicalEntity]:
        """
        Compute intermediates between two molecular functions.

        Example:

            >>> engine = GOReactionEngine()
            >>> gmer = "GO:0047918"
            >>> gmd = "GO:0008446"
            >>> intermediates = engine.compute_intermediates(gmer, gmd)
            >>> sorted(intermediates, key=lambda x: x.id)
            [ChemicalEntity(id='CHEBI:57527', label='GDP-alpha-D-mannose(2-)')]

        :param upstream_mf:
        :param downstream_mf:
        :return:
        """
        upstream_chemicals = set(self.mfs_to_chemicals([upstream_mf]))
        downstream_chemicals = set(self.mfs_to_chemicals([downstream_mf]))
        intermediates = upstream_chemicals.intersection(downstream_chemicals)
        return self._chebi_ids_to_entities(intermediates)






