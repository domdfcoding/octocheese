#!/usr/bin/env python3
#
#  cli.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on https://github.com/readthedocs/sphinx_rtd_theme/blob/master/docs/conf.py
#  Copyright (c) 2013-2018 Dave Snider, Read the Docs, Inc. & contributors
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import re
from argparse import ONE_OR_MORE, OPTIONAL, PARSER, REMAINDER, SUPPRESS, ZERO_OR_MORE
from typing import Any, Dict, List, Union

# 3rd party
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from domdf_python_tools.utils import strtobool
from sphinx.addnodes import desc_signature
from sphinx.application import Sphinx
from sphinx.domains import ObjType
from sphinx.domains.std import GenericObject, StandardDomain
from sphinx.errors import ExtensionError
from sphinx.roles import XRefRole
from sphinx_toolbox.utils import OptionSpec
from typing_extensions import TypedDict

__all__ = ["CLIArgument", "register_cli", "setup"]


class ArgumentMetadata(TypedDict):
	"""
	:class:`typing.TypedDict` representing the metadata for a cli argument.
	"""

	name_or_flags: List[str]
	type: str
	required: bool
	default: str
	nargs: Union[str, int, None]
	choices: List[str]
	metavar: str


class CLIArgument(GenericObject):
	"""
	The cli-arg directive.
	"""

	option_spec: OptionSpec = {  # type: ignore
		"type": directives.unchanged_required,  # The type of argument to supply.
		"required": strtobool,  # Whether or not the command-line option may be omitted (optionals only).
		"default": directives.unchanged_required,  # The value produced if the argument is absent from the command line.
		"nargs": directives.unchanged_required,  # The number of command-line arguments that should be consumed.
		"choices": directives.unchanged_required,  # A container of the allowable values for the argument.
		"metavar": directives.unchanged_required,  # A name for the argument in usage messages.
		}

	def __init__(
			self,
			name,
			arguments,
			options,
			content,
			lineno,
			content_offset,
			block_text,
			state,
			state_machine,
			):

		# metadata for the argument
		self.metadata: ArgumentMetadata = {
				"name_or_flags": [],
				"type": '',
				"required": False,
				"default": '',
				"nargs": None,
				"choices": [],
				"metavar": '',
				}

		super().__init__(
				name,
				arguments,
				options,
				content,
				lineno,
				content_offset,
				block_text,
				state,
				state_machine,
				)

	def _metavar_formatter(self, metadata):
		if metadata["metavar"] is not None:
			result = metadata["metavar"]
		elif metadata["choices"] is not None:
			choice_strs = [str(choice) for choice in metadata["choices"]]
			result = f"{{{','.join(choice_strs)}}}"
		else:
			result = ''

		def format(tuple_size):
			if isinstance(result, tuple):
				return result
			else:
				return (result, ) * tuple_size

		return format

	def format_args(self) -> str:
		get_metavar = self._metavar_formatter(self.metadata)

		nargs = self.metadata["nargs"]

		if nargs is None:
			result = f" {get_metavar(1)}"
		elif nargs == OPTIONAL:
			result = f" [{get_metavar(1)}]"
		elif nargs == ZERO_OR_MORE:
			result = " [{} [{} ...]]".format(get_metavar(2))
		elif nargs == ONE_OR_MORE:
			result = " {} [{} ...]".format(get_metavar(2))
		elif nargs == REMAINDER:
			result = " ..."
		elif nargs == PARSER:
			result = f" {get_metavar(1)} ..."
		elif nargs == SUPPRESS:
			result = ''
		else:
			try:
				formats = [" %s" for _ in range(nargs)]
			except TypeError:
				raise ValueError("invalid nargs value") from None
			result = ' '.join(formats) % get_metavar(nargs)
		return result.rstrip()

	def handle_signature(self, sig: str, signode: desc_signature) -> str:
		name_or_flags = re.split(r"[, ]", sig)
		self.metadata["name_or_flags"] = name_or_flags
		return super().handle_signature(", ".join(name_or_flags) + self.format_args(), signode)

	def run(self) -> List[Node]:
		"""
		Process the content of the directive.
		"""

		content = []

		if "type" in self.options:
			content.append(f"| **Type:** {self.options['type']}")
			self.metadata["type"] = self.options["type"]

		if "required" in self.options:
			required = strtobool(self.options["required"])
			content.append(f"| **Required:** ``{required}``")
			self.metadata["required"] = required

		if "default" in self.options:
			content.append(f"| **Default:** {self.options['default']}")
			self.metadata["default"] = self.options["default"]

		self.metadata["metavar"] = self.options.get("metavar", '').upper()
		self.metadata["choices"] = re.split(r"[, ]", self.options.get("metavar", ''))

		if "nargs" in self.options:
			nargs = self.options["nargs"]
			if nargs.is_digit():
				self.options["nargs"] = int(nargs)
			else:
				self.options["nargs"] = str(nargs)

		self.content = StringList(['', *content, '', *self.content])

		return super().run()


def register_cli(app: Sphinx, override: bool = False) -> None:
	"""
	Create and register the ``confval`` role and directive.

	:param app:
	:param override:
	"""

	if "std" not in app.registry.domains:
		app.add_domain(StandardDomain)  # pragma: no cover

	name = "cli-arg"

	app.registry.add_directive_to_domain("std", name, CLIArgument)
	app.registry.add_role_to_domain("std", name, XRefRole())

	object_types = app.registry.domain_object_types.setdefault("std", {})

	if name in object_types and not override:  # pragma: no cover
		raise ExtensionError(f"The {name!r} object_type is already registered")

	object_types[name] = ObjType(name, name)


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup :mod:`cli`.

	:param app:

	:return:
	"""

	# this package
	# from sphinx_toolbox import __version__

	register_cli(app)

	return {
			# "version": __version__,
			"parallel_read_safe": True,
			}
