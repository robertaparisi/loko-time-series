import {
  Button,
  Stack,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";
import { useContext } from "react";
import { CLIENT, StateContext } from "../../config/constants";
import { BaseForm } from "./BaseForm";

export function ModelCreation({ onClose }) {
  const _state = useContext(StateContext);
  return (
    <Stack w="80%" h="100%" spacing="2rem">
      <Button w="10%" onClick={onClose}>
        Close
      </Button>
      <Tabs>
        <TabList>
          {/* <Tab>Base</Tab>
          <Tab>Advanced</Tab> */}
          <Tab>Manual</Tab>
        </TabList>
        <TabPanels>
          {/* <TabPanel>Base</TabPanel>
          <TabPanel>Manual</TabPanel> */}
          <TabPanel>
            <BaseForm
              onSubmit={(name, data) => {
                console.log("Name", name);
                CLIENT.models[name]
                  .post(data)
                  .then((resp) => (_state.refresh = new Date()));
                onClose();
              }}
            />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Stack>
  );
}
