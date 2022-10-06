import { Box, Button, Flex, HStack, Spacer, Stack } from "@chakra-ui/react";
import { useCompositeState } from "ds4biz-core";
import { useState } from "react";
import reactLogo from "./assets/react.svg";
import { Model } from "./views/Model";
import { ModelCreation } from "./views/ModelCreation";

function App() {
  const state = useCompositeState({
    models: ["primo", "secondo", "terzo"],
    view: "list",
  });

  switch (state.view) {
    case "list":
      return (
        <Flex w="100vw" h="100vh" p="2rem">
          <Stack w="100%" h="100%" spacing="2rem">
            <HStack p="2rem">
              <Button onClick={(e) => (state.view = "model_creation")}>
                New model
              </Button>
            </HStack>

            <Stack>
              {state.models.map((name) => (
                <Model
                  onClick={(e) => (state.view = "model")}
                  name={name}
                  key={name}
                />
              ))}
            </Stack>
          </Stack>
        </Flex>
      );

    case "model":
      return (
        <Flex w="100vw" h="100vh" p="2rem">
          <Box onClick={(e) => (state.view = "list")}>Details</Box>
        </Flex>
      );
    case "model_creation":
      return (
        <Flex w="100vw" h="100vh" p="2rem">
          <ModelCreation onClose={(e) => (state.view = "list")} />
        </Flex>
      );
  }
}

export default App;
