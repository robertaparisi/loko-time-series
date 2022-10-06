import {
  Button,
  Stack,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";
import { BaseForm } from "./forms/BaseForm";

export function ModelCreation({ onClose }) {
  return (
    <Stack w="100%" h="100%" spacing="2rem">
      <Button w="10%" onClick={onClose}>
        Close
      </Button>
      <Tabs>
        <TabList>
          <Tab>Base</Tab>
          <Tab>Advanced</Tab>
          <Tab>Manual</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <BaseForm />
          </TabPanel>
          <TabPanel>Advanced</TabPanel>
          <TabPanel>Manual</TabPanel>
        </TabPanels>
      </Tabs>
    </Stack>
  );
}
