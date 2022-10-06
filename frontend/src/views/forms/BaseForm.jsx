import { Box, Input, Select, Stack, Text, Textarea } from "@chakra-ui/react";

export function BaseForm() {
  return (
    <Stack>
      <Text fontSize="xs">
        Name
        <Box as="span" color="red">
          *
        </Box>
      </Text>
      <Input type="text" />
      <Text fontSize="xs">
        Description
        <Box as="span" color="red">
          *
        </Box>
      </Text>
      <Textarea />
      <Text fontSize="xs">
        Model ID
        <Box as="span" color="red">
          *
        </Box>
      </Text>
      <Select>
        <option>A</option>
        <option>B</option>
      </Select>
      <Text fontSize="xs">
        Transformer ID
        <Box as="span" color="red">
          *
        </Box>
      </Text>
      <Select>
        <option>A</option>
        <option>B</option>
      </Select>
    </Stack>
  );
}
