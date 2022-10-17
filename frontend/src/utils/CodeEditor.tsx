import { json } from '@codemirror/lang-json';
import { useColorMode } from '@chakra-ui/react';
import ReactCodeMirror, { ReactCodeMirrorProps } from '@uiw/react-codemirror';
import { useCallback } from 'react';


export type Mode = 'json';


interface CodeEditorProps extends ReactCodeMirrorProps {
    mode?: Mode;
  }