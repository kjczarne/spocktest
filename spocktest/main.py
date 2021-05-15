import argparse
from spocktest.extract import extract
from spocktest.inject import inject
from spocktest.state import STATE
from spocktest.defaults import (
    SNIPPET_ID, SNIPPET_END, ID_TEMPLATE_REGEX,
    SNIPPET_INJECT, ALLOWED_DOC_EXTS, ALLOWED_CODE_EXTS
)
from loguru import logger

def main():
    parser = argparse.ArgumentParser(
        prog='spocktest', 
        description='Embed unit test snippets into human-readable documentation'
    )
    parser.add_argument(
        'input',
        help='Input directory/file with tests',
        type=str
    )
    parser.add_argument(
        'docs',
        help='Input directory/file with documentation',
        type=str
    )
    parser.add_argument(
        '-o', '--output',
        help='Output directory/file with documentation. ' + \
             'If not provided, the input docs folder will be ' + \
             'populated with snippets in-place',
        type=str
    )
    parser.add_argument(
        '-p', '--pattern',
        help='Regex pattern to match the IDs with ' + \
             '`{{ID}}` in place of the actual expected ID. ' + \
             f'The ID itself matches a `{ID_TEMPLATE_REGEX}` pattern. ' +
             'To override that, use `--id-text-regex` flag. ' + \
             f'The default value: `{SNIPPET_ID}`',
        type=str
    )
    parser.add_argument(
        '-e', '--end',
        help='Comment pattern to match that demarcates ' + \
             f'the end of a given snippet. Default: `{SNIPPET_END}`',
        type=str
    )
    parser.add_argument(
        '-x', '--doc-exts',
        help='List of documentation file extensions to be ' + \
             f'considered. Default: {ALLOWED_DOC_EXTS}',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '-c', '--code-exts',
        help='List of test file extensions to be ' + \
             f'considered. Default: {ALLOWED_CODE_EXTS}',
        nargs='+',
        type=str
    )
    parser.add_argument(
        '-t', '--target-pattern',
        help='Regex pattern to match the snippet placeholder ' + \
             'in the documentation files, with `{{ID}}` in place ' + \
             f'of the actual ID value. Default: `{SNIPPET_INJECT}`',
        type=str
    )
    parser.add_argument(
        '--id-regex-ovd',
        help=f'Overrides the default ID Regex (`{ID_TEMPLATE_REGEX}`) if for ' +
             'some reason you need a different one.',
        type=str
    )
    parser.add_argument(
        '--debug',
        help='Run in debug mode',
        type=bool
    )

    args = parser.parse_args()

    if args.debug:
        STATE.debug = True

    extract(
        args.input,
        args.pattern      if args.pattern else SNIPPET_ID,
        args.end          if args.end else SNIPPET_END,
        args.code_exts    if args.code_exts else ALLOWED_CODE_EXTS,
        args.id_regex_ovd if args.id_regex_ovd else ID_TEMPLATE_REGEX,
    )
    
    logger.info(f"Found: {len(STATE.snippets)} snippets")
    logger.info(f"Beginning injection...")
    
    inject(
        args.docs,
        args.target_pattern if args.target_pattern else SNIPPET_INJECT,
        STATE.snippets,
        args.output         if args.output else None,
        args.doc_exts       if args.doc_exts else ALLOWED_DOC_EXTS,
    )
    
    logger.info(f"Injected snippets into {STATE.placeholders_filled} total placeholders")
    

if __name__ == "__main__":
    main()
