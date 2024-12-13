import { Badge } from "@/components/ui/badge";
import type { StreamState } from "../_hooks/useStream";
import { Loader2Icon } from "lucide-react";

export function SectionLoader<T>({
  title,
  items,
  renderItem,
}: {
  title: string;
  items: T[] | null | undefined;
  renderItem: (item: T) => React.ReactNode;
}) {
  return (
    <section className="mb-8">
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      {items ? (
        items.map((item, i) => (
          <div
            key={`${title}-${
              // biome-ignore lint/suspicious/noArrayIndexKey: index is unique
              i
            }`}
            className="mb-4"
          >
            {renderItem(item)}
          </div>
        ))
      ) : (
        <LoadingText text={title.toLowerCase()} />
      )}
    </section>
  );
}

export function LoadingText({ text }: { text: string | null }) {
  return (
    <span className="text-muted-foreground flex items-center gap-2">
      <Loader2Icon className="animate-spin h-5 w-5" />
      {text ? `Loading ${text}...` : null}
    </span>
  );
}

export function RenderState({ res }: { res: StreamState<any> }) {
  switch (res.status) {
    case "idle":
      return null;
    case "loading":
      return <LoadingText text={null} />;
    case "error":
      if (res.error?.message.includes("BamlValidationError")) {
        return (
          <div className="text-red-500">
            You&apos;re being naughty!!
            <br />
            But that was a good try! 🤡
          </div>
        );
      }
      return (
        <div className="flex items-center gap-2 flex-col">
          <Badge variant="destructive">Error</Badge>
          <div className="text-sm text-muted-foreground">
            {res.error?.message}
          </div>
        </div>
      );
    case "success":
      return <Badge variant="default">Done</Badge>;
  }
  res.status satisfies never;
}
