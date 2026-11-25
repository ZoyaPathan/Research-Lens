import React, { useState } from "react";
import { MessageSquareText } from "lucide-react";
import { api } from "../api/client";

const DEFAULT_DISCOURSE =
  "Research in edge computing increasingly demands low-latency inference. However, existing models struggle with strict memory limits on microcontrollers. Therefore, we propose a quantized TinyML framework. Experimental results demonstrate a 41% latency reduction across industrial sensor streams. Overall, this approach enables practical real-time deployment.";

const DEFAULT_CONVERSATION =
  "Person A: Hi, are you coming to the research seminar today?\nPerson B: Hi! I have an examination tomorrow morning.\nPerson A: Could you share your slides with me later?\nPerson B: Sure, I will email them tonight.";

export const DiscoursePage: React.FC = () => {
  const [text, setText] = useState(DEFAULT_DISCOURSE);
  const [conversation, setConversation] = useState(DEFAULT_CONVERSATION);
  const [discRes, setDiscRes] = useState<any>(null);
  const [convRes, setConvRes] = useState<any>(null);
  const [error, setError] = useState("");

  const analyzeDiscourse = async () => {
    setError("");
    try {
      const data = await api.discourseAnalyze(text);
      setDiscRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Discourse analysis failed.");
    }
  };

  const analyzeConversation = async () => {
    setError("");
    try {
      const data = await api.discourseConversation(conversation);
      setConvRes(data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Conversation analysis failed.");
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <span className="text-xs font-semibold uppercase tracking-wider text-teal-700">Unit IV</span>
        <h1 className="text-xl font-bold text-slate-900">Discourse &amp; Pragmatic Analysis</h1>
        <p className="text-sm text-slate-600 mt-1">
          Educational rule-based demonstrations of Cohesion, Discourse Structure, Adjacency Pairs, Implicature, Cooperative Principle, Deixis, Endophora/Exophora, Speech Acts, and Pragmatic Markers &amp; Face.
        </p>
      </div>

      {error && <div className="card p-4 bg-red-50 border-red-200 text-red-700 text-sm">{error}</div>}

      {/* Academic Discourse Analysis */}
      <div className="card p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-900">
          Part 1: Academic Text Discourse (Cohesion, Structure, Deixis, Endophora, Speech Acts, Pragmatic Markers)
        </h2>
        <textarea
          rows={4}
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="input-field"
        />
        <div className="flex justify-end">
          <button onClick={analyzeDiscourse} className="btn-primary">
            <MessageSquareText className="w-4 h-4" /> Analyze Discourse
          </button>
        </div>

        {discRes && (
          <div className="space-y-4 pt-2 text-xs">
            <div className="p-2.5 rounded bg-amber-50 border border-amber-200 text-amber-800">
              {discRes.disclaimer}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
                <div className="font-semibold text-slate-800">A. Discourse Cohesion</div>
                <div><strong>Reference Words:</strong> {discRes.cohesion.reference_words.join(", ") || "—"}</div>
                <div><strong>Conjunctions:</strong> {discRes.cohesion.conjunctions.join(", ") || "—"}</div>
                <div><strong>Discourse Markers:</strong> {discRes.cohesion.discourse_markers.join(", ") || "—"}</div>
                <div>
                  <strong>Repeated Key Terms:</strong>{" "}
                  {discRes.cohesion.repeated_key_terms.map((t: any) => `${t.term} (${t.count})`).join(", ") || "—"}
                </div>
              </div>

              <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
                <div className="font-semibold text-slate-800">F. Deixis &amp; I. Pragmatic Markers</div>
                <div><strong>Person Deixis:</strong> {discRes.deixis.person.join(", ") || "—"}</div>
                <div><strong>Temporal Deixis:</strong> {discRes.deixis.temporal.join(", ") || "—"}</div>
                <div><strong>Demonstrative Deixis:</strong> {discRes.deixis.demonstrative.join(", ") || "—"}</div>
                <div><strong>Pragmatic Markers:</strong> {discRes.pragmatic_markers.detected.join(", ") || "—"}</div>
              </div>
            </div>

            <div className="p-4 bg-white rounded-lg border border-slate-200 space-y-2">
              <div className="font-semibold text-slate-800">B. Discourse Structure (Heuristic Predictions)</div>
              <div className="space-y-2">
                {discRes.discourse_structure.map((s: any) => (
                  <div key={s.index} className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-2.5 bg-slate-50 rounded border border-slate-100">
                    <span><strong>S{s.index}:</strong> {s.sentence}</span>
                    <span className="px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-medium shrink-0">
                      {s.predicted_role}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="p-4 bg-white rounded-lg border border-slate-200 space-y-2">
                <div className="font-semibold text-slate-800">G. Endophora (Anaphora / Cataphora) &amp; Exophora</div>
                {discRes.endophora_exophora.examples.map((ex: any, i: number) => (
                  <div key={i} className="p-2 bg-slate-50 rounded">
                    <div className="font-semibold text-slate-700">{ex.type}</div>
                    <div className="italic">"{ex.example}"</div>
                    <div className="text-slate-500">{ex.note}</div>
                  </div>
                ))}
              </div>

              <div className="p-4 bg-white rounded-lg border border-slate-200 space-y-2">
                <div className="font-semibold text-slate-800">H. Speech Acts &amp; Face Theory</div>
                {discRes.speech_acts.slice(0, 4).map((sa: any, i: number) => (
                  <div key={i} className="p-2 bg-slate-50 rounded">
                    <span className="font-semibold text-teal-700">{sa.act} ({sa.directness}):</span>{" "}
                    <span>{sa.sentence}</span>
                  </div>
                ))}
                <div className="pt-1 text-slate-600">
                  <div><strong>Positive Face:</strong> {discRes.pragmatic_markers.face_theory_examples.positive_face}</div>
                  <div><strong>Negative Face:</strong> {discRes.pragmatic_markers.face_theory_examples.negative_face}</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Conversational Pragmatics */}
      <div className="card p-5 space-y-4">
        <h2 className="text-sm font-semibold text-slate-900">
          Part 2: Conversational Pragmatics (Adjacency Pairs, Implicature &amp; Grice&apos;s Cooperative Principle)
        </h2>
        <textarea
          rows={4}
          value={conversation}
          onChange={(e) => setConversation(e.target.value)}
          className="input-field font-mono text-xs"
        />
        <div className="flex justify-end">
          <button onClick={analyzeConversation} className="btn-primary">
            Analyze Conversation
          </button>
        </div>

        {convRes && (
          <div className="space-y-4 pt-2 text-xs">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
                <div className="font-semibold text-slate-800">C. Adjacency Pairs</div>
                {convRes.adjacency_pairs.map((p: any, i: number) => (
                  <div key={i} className="p-2 bg-white rounded border border-slate-200">
                    <div className="font-semibold text-blue-700">{p.pair_type}</div>
                    <div>{p.first_turn}</div>
                    <div>{p.second_turn}</div>
                  </div>
                ))}
              </div>

              <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
                <div className="font-semibold text-slate-800">D. Conversational Implicature</div>
                {convRes.implicatures.length ? (
                  convRes.implicatures.map((imp: any, i: number) => (
                    <div key={i} className="p-2 bg-white rounded border border-slate-200 space-y-1">
                      <div className="font-medium">{imp.exchange}</div>
                      <div className="text-teal-800">{imp.possible_implied_meaning}</div>
                      <div className="text-[11px] text-amber-700">{imp.caveat}</div>
                    </div>
                  ))
                ) : (
                  <div className="text-slate-500">No indirect implicatures detected in this dialogue.</div>
                )}
              </div>
            </div>

            <div className="p-4 bg-white rounded-lg border border-slate-200 space-y-2">
              <div className="font-semibold text-slate-800">E. Grice&apos;s Cooperative Principle (Four Maxims)</div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
                {convRes.cooperative_principle.map((m: any) => (
                  <div key={m.maxim} className="p-3 bg-slate-50 rounded border border-slate-200 space-y-1">
                    <div className="font-semibold text-slate-900">Maxim of {m.maxim}</div>
                    <div className="text-slate-600">{m.principle}</div>
                    <div className="text-blue-700">{m.heuristic_observation}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
