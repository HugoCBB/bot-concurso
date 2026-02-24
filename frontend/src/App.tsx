import { useState, useEffect } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { MapPin, Briefcase, GraduationCap, Calendar, ExternalLink, AlertCircle, ChevronLeft, ChevronRight } from "lucide-react";
import { contestsApi } from "./services/api";

interface Contest {
  orgao: string;
  info: string;
  cargo: string;
  nivel: string;
  data_limite: string;
  link: string;
}

export default function App() {
  const [contests, setContests] = useState<Contest[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination State
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const pageSize = 12;

  useEffect(() => {
    const fetchContests = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await contestsApi.get_contests(currentPage, pageSize);

        let fetchedItems: Contest[] = [];
        let fetchedTotalPages = 1;

        if (data && data.items) {
          fetchedItems = data.items;
          // fastapi-pagination `Page` returns `pages` directly. If not, calculate it:
          fetchedTotalPages = data.pages || Math.ceil((data.total || 0) / pageSize) || 1;
        } else if (Array.isArray(data)) {
          // Fallback if backend isn't paginating correctly
          fetchedItems = data;
          fetchedTotalPages = Math.ceil(data.length / pageSize) || 1;
        }

        setContests(fetchedItems);
        setTotalPages(fetchedTotalPages);
      } catch (err: any) {
        setError(err.message || "Falha ao buscar os concursos.");
      } finally {
        setLoading(false);
      }
    };

    fetchContests();
  }, [currentPage]);

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage((prev) => prev + 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/30 pb-24">
      <main className="container mx-auto px-4 pt-12">
        <div className="mb-10 text-center space-y-4">
          <h2 className="text-4xl md:text-5xl font-extrabold tracking-tight">
            Vagas Abertas
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Acompanhe os principais concursos públicos disponíveis e garanta a sua aprovação.
          </p>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="overflow-hidden">
                <CardHeader className="pb-4">
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
                <CardContent className="space-y-3">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-5/6" />
                  <Skeleton className="h-4 w-4/6" />
                </CardContent>
                <CardFooter>
                  <Skeleton className="h-10 w-full" />
                </CardFooter>
              </Card>
            ))}
          </div>
        ) : error ? (
          <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="w-16 h-16 rounded-full bg-destructive/10 flex items-center justify-center mb-4">
              <AlertCircle className="w-8 h-8 text-destructive" />
            </div>
            <h3 className="text-2xl font-bold mb-2">Erro ao carregar dados</h3>
            <p className="text-muted-foreground">{error}</p>
            <Button className="mt-6" variant="outline" onClick={() => window.location.reload()}>
              Tentar Novamente
            </Button>
          </div>
        ) : contests.length === 0 ? (
          <div className="text-center py-20 text-muted-foreground">
            Nenhum concurso encontrado.
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              {contests.map((contest, index) => (
                <Card
                  key={index}
                  className="group flex flex-col h-full overflow-hidden border-border/50 bg-card hover:shadow-xl hover:shadow-primary/10 hover:border-primary/30 transition-all duration-300"
                >
                  <div className="h-2 w-full bg-gradient-to-r from-primary to-accent opacity-80 group-hover:opacity-100 transition-opacity" />
                  <CardHeader className="pb-4 flex-none">
                    <Badge variant="secondary" className="w-fit mb-3 bg-primary/10 text-primary border-0 hover:bg-primary/20">
                      <MapPin className="w-3 h-3 mr-1" />
                      {contest.info.substring(0, 2) === "SP" || contest.info.substring(0, 2) === "RJ" || contest.info.substring(0, 2) === "MG"
                        ? contest.info.substring(0, 2)
                        : "Nacional/Estadual"}
                    </Badge>
                    <CardTitle className="text-xl leading-tight group-hover:text-primary transition-colors">
                      {contest.orgao}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 flex-1">
                    <div className="flex items-start gap-3">
                      <Briefcase className="w-5 h-5 text-muted-foreground shrink-0 mt-0.5" />
                      <div className="grid gap-0.5">
                        <span className="text-sm font-medium leading-tight">Cargo</span>
                        <span className="text-sm text-muted-foreground">{contest.cargo}</span>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <GraduationCap className="w-5 h-5 text-muted-foreground shrink-0 mt-0.5" />
                      <div className="grid gap-0.5">
                        <span className="text-sm font-medium leading-tight">Nível</span>
                        <span className="text-sm text-muted-foreground">{contest.nivel}</span>
                      </div>
                    </div>

                    <div className="flex items-start gap-3">
                      <Calendar className="w-5 h-5 text-muted-foreground shrink-0 mt-0.5" />
                      <div className="grid gap-0.5">
                        <span className="text-sm font-medium leading-tight">Vagas e Salário</span>
                        <span className="text-sm text-muted-foreground">{contest.info}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 mt-4 pt-4 border-t border-border/50">
                      <span className="text-sm font-semibold text-destructive flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-destructive animate-pulse" />
                        Até: {contest.data_limite}
                      </span>
                    </div>
                  </CardContent>
                  <CardFooter className="pt-0 flex-none">
                    <Button asChild className="w-full rounded-xl gap-2 font-medium" variant="default">
                      <a href={contest.link} target="_blank" rel="noopener noreferrer">
                        Ver Edital <ExternalLink className="w-4 h-4" />
                      </a>
                    </Button>
                  </CardFooter>
                </Card>
              ))}
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-4 mt-8">
                <Button
                  variant="outline"
                  onClick={handlePrevPage}
                  disabled={currentPage === 1}
                  className="rounded-full"
                >
                  <ChevronLeft className="w-4 h-4 mr-2" />
                  Anterior
                </Button>

                <span className="text-sm font-medium">
                  Página {currentPage} de {totalPages}
                </span>

                <Button
                  variant="outline"
                  onClick={handleNextPage}
                  disabled={currentPage === totalPages}
                  className="rounded-full"
                >
                  Próxima
                  <ChevronRight className="w-4 h-4 ml-2" />
                </Button>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

