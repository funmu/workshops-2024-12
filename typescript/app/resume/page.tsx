"use client";

import { useMemo, useState } from "react";
import { extractResume } from "../_actions/ai-actions";
import { RenderState } from "../_components/section-loader";
import { useStream } from "../_hooks/useStream";
import { PartialResumeComponent } from "./resume-component";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Resume() {
  const [rawResume, setRawResume] = useState<string>("");
  const structuredResume = useStream(extractResume);

  const response = useMemo(() => {
    if (structuredResume.status === "error") {
      return null;
    }
    if (structuredResume.status === "success") {
      return structuredResume.streamingData;
    }
    return structuredResume.data;
  }, [
    structuredResume.status,
    structuredResume.streamingData,
    structuredResume.data,
  ]);

  return (
    <div className="container max-w-[1800px] mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold text-center mb-8">Resume Parser</h1>
      <div className="grid grid-cols-2 gap-4">
        <Card className="shadow-lg h-[calc(100vh-12rem)]">
          <CardHeader>
            <CardTitle className="text-xl">Input Resume Text</CardTitle>
          </CardHeader>
          <CardContent>
            <UserInput
              value={rawResume}
              onChange={setRawResume}
              onSubmit={() => structuredResume.mutate(rawResume)}
            />
          </CardContent>
        </Card>

        <Card className="shadow-lg h-[calc(100vh-12rem)] overflow-auto">
          <CardHeader>
            <CardTitle className="text-xl">Pretty Resume</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <RenderState res={structuredResume} />
              {response ? <PartialResumeComponent resume={response} /> : null}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

const UserInput = ({
  value,
  onChange,
  onSubmit,
}: {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
}) => {
  return (
    <div className="flex flex-col h-full gap-4">
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste your resume text here..."
        className="flex-1 resize-none"
      />
      <Button onClick={onSubmit} className="w-full" size="lg">
        Parse Resume
      </Button>
    </div>
  );
};
