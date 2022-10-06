import { Button, Flex, HStack, Stack } from "@chakra-ui/react";
import { useCompositeState } from "ds4biz-core";
import { useContext } from "react";
import { CLIENT, StateContext } from "../../config/constants";
import { Model } from "./Model";
import { ModelCreation } from "./ModelCreation";

export function Models({ models }) {
  const state = useCompositeState({ view: "list" });
  const _state = useContext(StateContext);
  switch (state.view) {
    case "list":
      return (
        <Stack w="100%" h="100%" spacing="2rem">
          <HStack>
            <Button onClick={(e) => (state.view = "new")}>New model</Button>
          </HStack>

          <Stack>
            {models.map((name) => (
              <Model
                //onClick={(e) => (state.view = "model")}
                name={name}
                key={name}
                onDelete={(e) =>
                  CLIENT.models[name].delete().then((resp) => {
                    _state.refresh = new Date();
                  })
                }
              />
            ))}
          </Stack>
        </Stack>
      );
    case "new":
      return (
        <Flex w="100vw" h="100vh" p="2rem">
          <ModelCreation onClose={(e) => (state.view = "list")} />
        </Flex>
      );

    default:
      break;
  }
}
