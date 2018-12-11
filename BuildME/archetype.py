"""
Archetype management
"""

__author__ = "Niko Heeren"
__email__ = "niko.heeren@gmail.com"
__license__ = "MIT"
__copyright__ = "Niko Heeren 2018"
__version__ = "0.1"
__status__ = "ALPHA"

import eppy


def apply_material_substitution(idf, mat, mate_new):
    """
    Replaces a given material in the archetype.
    :param idf: Eppy idf class
    :param mat: Material to be substituted
    :param mate_new: object
    :return:
    """
    pass


def apply_lightweighting():
    pass


def apply_more_intense_use(idf, new_occ, assert_occ=None):
    """
    Applies the RE strategy "More intense use".
    :param idf:
    :param new_occ: New building occupation to apply.
    :param assert_occ: Check if the occupation has an expected value.
    :return:
    """
    if assert_occ is not None:
        pass
    pass


def get_matrial_inventory():
    pass

