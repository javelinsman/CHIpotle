import {
  Button,
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Form,
  Heading,
  List,
  TextInput,
} from "grommet";
import * as Icons from "grommet-icons";
import React, { useState } from "react";
import { actionOverview } from "../redux/action/overview-actions";
import { useThunkDispatch } from "../redux/action/root-action";
import { useRootSelector } from "../redux/state/root-state";

const SearchBox: React.FC = () => {
  const [currentKeyword, setCurrentKeyword] = useState("");
  const keywords = useRootSelector((state) => state.overview.keywords);
  const seedPapers = useRootSelector((state) => state.overview.seedPapers);
  const dispatch = useThunkDispatch();

  return (
    <Card height="100%" width="100%" background="white">
      <CardHeader pad="small">
        <Heading level="4">Search Box</Heading>
      </CardHeader>
      <CardBody pad="small" gap="small">
        <Heading level="5">Keywords</Heading>
        <Form
          onSubmit={() => {
            dispatch(actionOverview.setKeywords([...keywords, currentKeyword]));
            setCurrentKeyword("");
          }}
        >
          <TextInput
            value={currentKeyword}
            onChange={(e) => setCurrentKeyword(e.target.value)}
          />
          <List
            data={keywords.map((keyword) => ({ entry: keyword }))}
            primaryKey={(item) => item.entry}
            pad={{ left: "small", right: "none", top: "none", bottom: "none" }}
            action={(item, index) => {
              return (
                <Button
                  icon={<Icons.Close size="small" />}
                  hoverIndicator
                  onClick={() => {
                    dispatch(
                      actionOverview.setKeywords(
                        keywords.filter((k) => k !== item.entry)
                      )
                    );
                  }}
                />
              );
            }}
          />
        </Form>
        <Heading level="5">Seed papers</Heading>
        <Form onSubmit={() => {}}>
          <List
            data={seedPapers.map((entry) => entry)}
            primaryKey={(entry) => entry.title}
            pad={{ left: "small", right: "none", top: "none", bottom: "none" }}
            action={(entry, index) => {
              return (
                <Button
                  icon={<Icons.Close size="small" />}
                  hoverIndicator
                  onClick={() => {
                    dispatch(
                      actionOverview.setSeedPapers(
                        seedPapers.filter((e) => e !== entry)
                      )
                    );
                  }}
                />
              );
            }}
          />
        </Form>
      </CardBody>
      <CardFooter
        pad={{ horizontal: "small" }}
        background="light-1"
        justify="end"
      >
        <Button
          onClick={() => {}}
          icon={<Icons.Search color="plain" />}
          hoverIndicator
        />
      </CardFooter>
    </Card>
  );
};

export default SearchBox;