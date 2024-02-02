#!/usr/bin/env python3
# encoding: utf-8
"""
@version: v1.0
@author: WESOFT
"""


class FrameworkException(Exception):
    """
    Base framework exception.
    """
    pass


class AssertionException(Exception):
    """
    Throw when case assert fail
    """
    pass


class ManuallyInterrupt(Exception):
    """
    Throw when manually click Cancel in the pop up dialog
    """


class ElementNoFoundException(Exception):
    """
    Throw when manually click Cancel in the pop up dialog
    """



