"use client";

import type { Resume } from "@/baml_client/types";
import type { RecursivePartialNull } from "@/baml_client/async_client";
import { SectionLoader, LoadingText } from "@/app/_components/section-loader";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  EnvelopeClosedIcon,
  PersonIcon,
  StarIcon,
  BackpackIcon,
  LightningBoltIcon,
} from "@radix-ui/react-icons";

export function PartialResumeComponent({
  resume,
}: {
  resume: RecursivePartialNull<Resume>;
}) {
  return (
    <div className="space-y-6">
      {/* Basic Information */}
      <Card className="border-none shadow-none">
        <CardContent className="space-y-4">
          <div className="flex items-center gap-2">
            <PersonIcon className="h-5 w-5 text-muted-foreground" />
            <h1 className="text-2xl font-semibold">
              {resume.name ?? <LoadingText text="name" />}
            </h1>
          </div>
          <div className="flex items-center gap-2 text-muted-foreground">
            <EnvelopeClosedIcon className="h-4 w-4" />
            <p>{resume.email ?? <LoadingText text="email" />}</p>
          </div>
        </CardContent>
      </Card>

      {/* Experience Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <BackpackIcon className="h-5 w-5" />
            <CardTitle>Experience</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <SectionLoader
            title=""
            items={resume.experience}
            renderItem={(exp) => (
              <div className="border-l-2 border-muted pl-4 py-2">
                {exp ?? <LoadingText text="experience" />}
              </div>
            )}
          />
        </CardContent>
      </Card>

      {/* Skills Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <LightningBoltIcon className="h-5 w-5" />
            <CardTitle>Skills</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            <SectionLoader
              title=""
              items={resume.skills}
              renderItem={(skill) => (
                <Badge variant="secondary">
                  {skill ?? <LoadingText text="skill" />}
                </Badge>
              )}
            />
          </div>
        </CardContent>
      </Card>

      {/* Why Hire Me Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <StarIcon className="h-5 w-5" />
            <CardTitle>Why You Should Hire Me</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <SectionLoader
            title=""
            items={resume.reason_to_hire}
            renderItem={(reason) => (
              <div className="space-y-2">
                <p className="text-sm">
                  {reason?.reason ?? <LoadingText text="reason" />}
                </p>
                {reason?.quote && (
                  <blockquote className="border-l-2 border-muted pl-4 italic text-muted-foreground">
                    {reason.quote}
                  </blockquote>
                )}
              </div>
            )}
          />
        </CardContent>
      </Card>
    </div>
  );
}

export function ResumeComponent({ resume }: { resume: Resume }) {
  return <PartialResumeComponent resume={resume} />;
}
